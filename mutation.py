from program import random
def swapMutation(children):
    for child in children:
        if (random.random()<0.2):
            indexToChange=(random.randint(0,len(child)-1),random.randint(0,len(child)-1))
            child[indexToChange[0]],child[indexToChange[1]]=child[indexToChange[1]],child[indexToChange[0]]
    return children
def newDefaultMutation(children):
    for i in range(len(children)):
        for j in range(len(children[i])):
            if(random.random()<0.05): # Mutation
                children[i][j]=random.randint(0,6)
    return children
def inversion(children):
    for child in children:
        if (random.random()<0.05):
            value=random.randint(0,len(child)//2)
            interval=(value,value+random.randint(0,len(child)//2))
            child[interval[0]:interval[1]]=child[interval[1]-1:interval[0]-1:-1]
    return children
