import random
import itertools

start=(0,0)
def generateStrategies(n):
    strategies=[]
    for strategy in range(n):
        randomlist = [random.randint(0,6)  for number in range(243)]
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
    It considers the following aspects:
    - The status of the cell is defined for the numbers  0: empty, 1: can: 2: wall
    - The id of the neighbor cells are defined for ; 0: north, 1: south, 2: west, 3: east, 4: north, 5:current site

    """
    numberOfActions=200
    cleaningSessions=100
    somelists=[[0,1,2] for i in range(5)] 
    perceptions= [list(element) for element in itertools.product(*somelists)]
    firstStrategies = generateStrategies(200)
    strategies= firstStrategies
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

def getNorth(position,board):
    newPos = (position[0],position[1]-1)
    if(newPos[1]<0):
        return 2
    elif(board[newPos[0]][newPos[1]]):
        return 1
    return 0
def getSouth(position,board):
    newPos = (position[0],position[1]+1)
    if(newPos[1]>9):
        return 2
    elif(board[newPos[0]][newPos[1]]):
        return 1
    return 0
def getWest(position,board):
    newPos = (position[0]-1,position[1])
    if(newPos[1]<0):
        return 2
    elif(board[newPos[0]][newPos[1]]):
        return 1
    return 0
def getEast(position,board):
    newPos = (position[0]+1,position[1])
    if(newPos[1]>9):
        return 2
    elif(board[newPos[0]][newPos[1]]):
        return 1
    return 0
def getCurrent(position,board):
    if(position[0]>9 or position[1]>9 or position[0]<0 or position[1]<0):
        return 2
    elif(board[position[0]][position[1]]):
        return 1
    return 0
def getSouth(position):
    pass
def getWest(position):
    pass
def getEast(position):
    pass
def getCurrent(position):
    pass

if __name__ == '__main__':
    run()