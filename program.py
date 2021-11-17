import random
import itertools
import numpy as np
import time
import csv
import plotly.express as px
import pandas as pd
import concurrent.futures


start=(0,0)
def getFitnessFromNumberOfSesions(strategy,numberOfSessions,numberOfActions,perceptions):
    fitness=0
    N=3
    for sesion in range(numberOfSessions):
        position=list(start)  
        board = generateBoard(N)     
        for iteration in range(numberOfActions):
            actualPerception=[getNorth(position,board,N),
                            getSouth(position,board,N),
                            getWest(position,board,N),
                            getEast(position,board,N),
                            getCurrent(position,board,N)
                            ]
            status=perceptions.index(actualPerception)
            action=strategy[status]
            fitness,board,position= applyAction(action,fitness,board,position,N)
    return fitness
def getFitness(strategy,cleaningSessions,numberOfActions,perceptions):
    fitness=0
    numberOfThreads =50 # This must be divisor of cleaningSessions 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results= [executor.submit(getFitnessFromNumberOfSesions,
         strategy,
         int(cleaningSessions/numberOfThreads),
                numberOfActions,
                perceptions
                ) for _ in range(numberOfThreads)]
        for f in concurrent.futures.as_completed(results):
            fitness+=f.result()
    fitness/=cleaningSessions
    return fitness
def trySomeStrategies(strategies,cleaningSessions,numberOfActions,perceptions):
    population=[]
    for strategy in strategies:
        fitness = getFitness(strategy,cleaningSessions,numberOfActions,perceptions)
        population.append((strategy,fitness))
    return population
def tryAllStrategies(strategies,population,cleaningSessions,numberOfActions,perceptions):
    division=2
    with concurrent.futures.ProcessPoolExecutor(max_workers=division) as executor:
        lenStrategies=len(strategies)
        someStrategies=[]
        for i in range(division):
            someStrategies.append(strategies[int(i*lenStrategies/division):int((i+1)*lenStrategies/division)])
        results = [executor.submit(trySomeStrategies,someStrategies[i],cleaningSessions,numberOfActions,perceptions) for i in range(division)]
        for f in concurrent.futures.as_completed(results):
            population+=f.result()
    return population
def defaultMutation(children):
    for i in range(len(children)):
        if(random.random()<0.01): # Mutation
            children[i][random.randint(0,len(children[i])-1)]=random.randint(0,6)
    return children
def generateStrategies(n,length):
    strategies=[]
    for strategy in range(n):
        randomlist = [random.randint(0,6)  for number in range(length)]
        strategies.append(randomlist)
    return strategies
def generateBoard(N):
    board=[]
    putCan = lambda : int(random.random()>0.5)
    for i in range(N):
        line = [putCan() for j in range(N)]
        board.append(line)
    return board

def run(f,perceptions,mutationFunction=defaultMutation):
    """
    Main function
    It considers the following aspects to execute the genetic algorithm:
    - The status of the cell is defined for the numbers  0: empty, 1: can: 2: wall
    - The id of the neighbor cells are defined for ; 0: north, 1: south, 2: west, 3: east, 4: current site
    - The actions based on the strategy are: 0: MoveNorth, 1: MoveSouth, 2: MoveWest, 3: MoveEast, 4: StayPut, 5: PickUp, 6: MoveRandom 
    
    To improve the performance, it uses multiprocessing and threads. It will consume a lot of memory and CPU 
    """
    writer = csv.writer(f)
    timeStart = 0
    timeStart = time.time()
    numberOfActions=100
    cleaningSessions=100
    firstStrategies = generateStrategies(200,len(perceptions))
    print(f"""Robby the robot - Genetic algorithm
    
    With size gene of {len(perceptions)} \n""")
    strategies= firstStrategies
    maxFitness=[]
    population=[]
    for generation in range(1000):
        print("Starting generation ",generation)
        population = tryAllStrategies(strategies,population,cleaningSessions,numberOfActions,perceptions)
        population.sort(reverse=True,key=lambda y: y[1])
        maxFitness.append(population[0][1]) #for painting
        writer.writerow([generation,population[0][0],population[0][1]])
        newStrategies=[]
        lengthPopulation = len(population)
        fitnessValues=[population[i][1] for i in range(lengthPopulation)]
        probabilities=getProbabilities(fitnessValues)
        while(len(newStrategies)<200):
            parents=np.random.choice(lengthPopulation, 2, p=probabilities) 
            father,mother = population[parents[0]],population[parents[1]]
            children = mate(father[0],mother[0],mutationFunction) 
            newStrategies.append(children[0])
            newStrategies.append(children[1])
        strategies=newStrategies
        population=[]
        print("Generation",generation,"=",maxFitness[generation])
        print("Execution time: ", round(time.time() - timeStart, 4), "seconds")
    f.close()    

def getNorth(position,board,N):
    newPos = (position[0],position[1]-1)
    if(newPos[1]<0):
        return 2
    return board[newPos[0]][newPos[1]]
def getSouth(position,board,N):
    newPos = (position[0],position[1]+1)
    if(newPos[1]>N-1):
        return 2
    return board[newPos[0]][newPos[1]]
def getWest(position,board,N):
    newPos = (position[0]-1,position[1])
    if(newPos[0]<0):
        return 2
    return board[newPos[0]][newPos[1]]
def getEast(position,board,N):
    newPos = (position[0]+1,position[1])
    if(newPos[0]>N-1):
        return 2
    return board[newPos[0]][newPos[1]]
def getCurrent(position,board,N):
    if(position[0]>N-1 or position[1]>N-1 or position[0]<0 or position[1]<0):
        return 2
    return board[position[0]][position[1]]

def applyAction(action,fitness,board,position,N):
    if action==0:
        newPos=(position[0],position[1]-1)
        if(newPos[1]<0):
            fitness-=5
            newPos = position
    elif action==1:
        newPos=(position[0],position[1]+1)
        if(newPos[1]>N-1):
            fitness-=5
            newPos = position
    elif action==2:
        newPos = (position[0]-1,position[1])
        if(newPos[0]<0):
            fitness-=5
            newPos = position
    elif action==3:
        newPos = (position[0]+1,position[1])
        if(newPos[0]>N-1):
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
        return applyAction(randAction,fitness,board,position,N)
    return (fitness,board,newPos)
def mate(father,mother,mutationFunction=defaultMutation):
    genXY,genXX=father,mother
    num=random.randint(0,len(father)-1)
    children=[
        genXY[:num]+genXX[num:],
        genXX[:num]+genXY[num:]
    ]
    children=mutationFunction(children)
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