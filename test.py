import random

def generateStrategies(n,length):
    strategies=[]
    for strategy in range(n):
        print(strategy)
        randomlist = [random.randint(0,6)  for _ in range(length)]
        strategies.append(randomlist)
    return strategies

print(generateStrategies(10,5))