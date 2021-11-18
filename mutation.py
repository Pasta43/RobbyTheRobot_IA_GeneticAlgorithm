from program import random
def swapMutation(children):
    if (random.random()<0.05):
        indexToChange=(random.randint(0,len(children[0])-1),random.randint(0,len(children[0])-1))
        children[0][indexToChange[0]],children[0][indexToChange[1]]=children[0][indexToChange[1]],children[0][indexToChange[0]]
        children[1][indexToChange[0]],children[1][indexToChange[1]]=children[1][indexToChange[1]],children[1][indexToChange[0]]
    return children