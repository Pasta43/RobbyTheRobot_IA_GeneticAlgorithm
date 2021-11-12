import random
import itertools
import numpy as np
import time
import csv
import plotly.express as px
import pandas as pd



start=(0,0)



def generateStrategies(n,length):
    strategies=[]
    for strategy in range(n):
        randomlist = [random.randint(0,6)  for number in range(length)]
        strategies.append(randomlist)
    return strategies
def generateBoard():
    board=[]
    putCan = lambda : int(random.random()>0.5)
    for i in range(10):
        line = [putCan() for j in range(10)]
        board.append(line)
    return board

def run(f,perceptions):
    """
    Main function
    It considers the following aspects to execute the genetic algorithm:
    - The status of the cell is defined for the numbers  0: empty, 1: can: 2: wall
    - The id of the neighbor cells are defined for ; 0: north, 1: south, 2: west, 3: east, 4: current site
    - The actions based on the strategy are: 0: MoveNorth, 1: MoveSouth, 2: MoveWest, 3: MoveEast, 4: StayPut, 5: PickUp, 6: MoveRandom 
    """
    writer = csv.writer(f)
    timeStart = 0
    timeStart = time.time()
    numberOfActions=200
    cleaningSessions=100
    firstStrategies = generateStrategies(200,len(perceptions))
    strategies= firstStrategies
    maxFitness=[]
    population=[]
    for generation in range(1000):
        print("Starting generation ",generation)
        for strategy in strategies:
            fitness=0
            for sesion in range(cleaningSessions):
                position=list(start)  
                board = generateBoard()     
                for iteration in range(numberOfActions):
                    actualPerception=[getNorth(position,board),
                                    getSouth(position,board),
                                    getWest(position,board),
                                    getEast(position,board),
                                    getCurrent(position,board)
                                    ]
                    status=perceptions.index(actualPerception)
                    action=strategy[status]
                    fitness,board,position= applyAction(action,fitness,board,position)
            fitness/=cleaningSessions
            population.append((strategy,fitness))
        population.sort(reverse=True,key=lambda y: y[1])
        maxFitness.append(population[0][1]) #for painting
        writer.writerow([generation,population[0][0],population[0][1]])
        newStrategies=[]
        fitnessValues=[population[i][1] for i in range(len(population))]
        probabilities=getProbabilities(fitnessValues)
        while(len(newStrategies)<200):
            parents=np.random.choice(len(population), 2, p=probabilities) 
            father,mother = population[parents[0]],population[parents[1]]
            children = mate(father[0],mother[0]) 
            newStrategies.append(children[0])
            newStrategies.append(children[1])
        strategies=newStrategies
        population=[]
        print("Generation",generation,"=",maxFitness[generation])
        print("Execution time: ", round(time.time() - timeStart, 4), "seconds")
    f.close()    

def getNorth(position,board):
    newPos = (position[0],position[1]-1)
    if(newPos[1]<0):
        return 2
    return board[newPos[0]][newPos[1]]
def getSouth(position,board):
    newPos = (position[0],position[1]+1)
    if(newPos[1]>9):
        return 2
    return board[newPos[0]][newPos[1]]
def getWest(position,board):
    newPos = (position[0]-1,position[1])
    if(newPos[0]<0):
        return 2
    return board[newPos[0]][newPos[1]]
def getEast(position,board):
    newPos = (position[0]+1,position[1])
    if(newPos[0]>9):
        return 2
    return board[newPos[0]][newPos[1]]
def getCurrent(position,board):
    if(position[0]>9 or position[1]>9 or position[0]<0 or position[1]<0):
        return 2
    return board[position[0]][position[1]]

def applyAction(action,fitness,board,position):
    if action==0:
        newPos=(position[0],position[1]-1)
        if(newPos[1]<0):
            fitness-=5
            newPos = position
    elif action==1:
        newPos=(position[0],position[1]+1)
        if(newPos[1]>9):
            fitness-=5
            newPos = position
    elif action==2:
        newPos = (position[0]-1,position[1])
        if(newPos[0]<0):
            fitness-=5
            newPos = position
    elif action==3:
        newPos = (position[0]+1,position[1])
        if(newPos[0]>9):
            fitness-=5
            newPos = position
    elif action==4:
        newPos = position                    
    elif action==5:
        newPos = position
        if(board[position[0]][position[1]]):
            fitness+=10
            board[position[0]][position[1]]=0
        else:
            fitness-=1
    elif action==6:
        randAction = random.randint(0,3)
        return applyAction(randAction,fitness,board,position)
    return (fitness,board,newPos)
def mate(father,mother):
    genXY,genXX=father,mother
    num=random.randint(0,len(father)-1)
    children=[
        genXY[:num]+genXX[num:],
        genXX[:num]+genXY[num:]
    ]
    for i in range(len(children)):
        if(random.random()<0.01): # Mutation
            children[i][random.randint(0,len(children[i])-1)]=random.randint(0,6)
    return children
def getProbabilities(fitnessValues):
    maxValue=max(fitnessValues)
    minValue=min(fitnessValues)
    normalized = list(
        map(
            lambda x: (x - minValue) / (maxValue - minValue),
            fitnessValues
        )
    )
    total = sum(normalized)
    probabilities=list(map(lambda x: x/total, normalized))
    print(sum(probabilities))
    probabilities.sort(reverse=True)
    return probabilities

def plotFitnes (fitnesScore):
    generation = [fitnesScore.index(n) + 1 for n in fitnesScore]

    df = pd.DataFrame(dict(
        Generation = generation,
        y = fitnesScore
    ))
    fig = px.line(df, x="Generation", y="y", title="Fitness vs Generation", markers=True,
                labels = {
                    "y": "Best fitness in population"
                }) 
    fig.show()

plotFitnes(fitnesScore)
if __name__ == '__main__':
    f = open("generationData.csv","w")
    somelists=[[0,1,2] for i in range(5)] 
    perceptions= [list(element) for element in itertools.product(*somelists)]
    run(f,perceptions)