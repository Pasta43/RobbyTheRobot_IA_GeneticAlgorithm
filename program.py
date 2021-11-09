import random

start=(0,0)
        
class Robby:
    def __init__(self):
        self.score=0
        self.current=(0,0)


def generateStrategies(n):
    strategies=[]
    for strategy in range(n):
        randomlist = [random.randint(0,6)  for number in range(n)]
        strategies.append(randomlist)
    return strategies

strategies = generateStrategies(200)
print(strategies[0])
print(strategies[1])