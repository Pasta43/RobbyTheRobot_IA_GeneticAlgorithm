from program import random
def swapMutation(children):
    for child in children:
        if (random.random()<0.2):
            indexToChange=(random.randint(0,len(child)-1),random.randint(0,len(child)-1))
            child[indexToChange[0]],child[indexToChange[1]]=child[indexToChange[1]],child[indexToChange[0]]
    return children