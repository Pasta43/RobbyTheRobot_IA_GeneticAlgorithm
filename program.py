import random
import itertools
import numpy as np
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

def run():
    """
    Main function
    It considers the following aspects to execute the genetic algorithm:
    - The status of the cell is defined for the numbers  0: empty, 1: can: 2: wall
    - The id of the neighbor cells are defined for ; 0: north, 1: south, 2: west, 3: east, 4: current site
    - The actions based on the strategy are: 0: MoveNorth, 1: MoveSouth, 2: MoveWest, 3: MoveEast, 4: StayPut, 5: PickUp, 6: MoveRandom 
    """
    numberOfActions=200
    cleaningSessions=100
    somelists=[[0,1,2] for i in range(5)] 
    perceptions= [list(element) for element in itertools.product(*somelists)]
    firstStrategies = generateStrategies(200,len(perceptions))
    strategies= firstStrategies
    maxFitness=[]
    fitnessValues=[]
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
        fitnessValues.append(fitness)  
    maxFitness.append(max(fitnessValues)) #for painting
    np.random.choice(strategies, 2, p=[0.1, 0.2, 0.3, 0.4])


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
    if(newPos[1]<0):
        return 2
    return board[newPos[0]][newPos[1]]
def getEast(position,board):
    newPos = (position[0]+1,position[1])
    if(newPos[1]>9):
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

if __name__ == '__main__':
    run()