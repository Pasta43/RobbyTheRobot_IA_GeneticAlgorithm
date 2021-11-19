from reduccion import removePerceptions, itertools, program,random
import numpy as np

class  c ():
    def __init__(self, c = 0 ):
        self._c = c
    
    def getC(self):
        return self._c

    def setC(self, x):
        self._c = x

def single_point_crossover(A, B, x):
    A_new = A[:x]+ B[x:]
    B_new = B[:x]+ A[x:]
    return A_new, B_new
            
def uniform_crossover(A, B, P):
    for i in range(len(P)):
        if P[i] < 0.3:
            temp = A[i]
            A[i] = B[i]
            B[i] = temp 
    return A, B
c = c()
def multi_point_crossover(children):
    c.setC(c.getC()+1)
    size = random.randint(0,len(children[0])//6)
    X = [random.randint(0,6) for _ in range(size)]
    Y = [random.randint(0,1000000) for _ in range(50)]
    if(c.getC() in Y):
        print("\n### Virus infection ###\n")
        viruses = [random.randint(0,6) for _ in range(size)]
        randomValue=random.randint(0,len(children[0])//2)
        children[0][randomValue:randomValue+size]=viruses
        children[1][randomValue:randomValue+size]=viruses
    elif (random.random()<0.3):
        for i in X:
            children[0], children[1] = single_point_crossover(children[0], children[1], i)
            children[0], children[1] = uniform_crossover(children[0], children[1] , np.random.rand(i)) 
    if(random.random()<0.3):
        children[0][0] = random.randint(0,6)
        children[1][0] = random.randint(0,6)
    return children

if __name__=="__main__":
    f = open("dataGenerationWithCrossover.csv","w")
    somelists=[[0,1,2] for i in range(5)] 
    perceptions= [list(element) for element in itertools.product(*somelists)]
    perceptions = removePerceptions(perceptions)
    program.run(f,perceptions,multi_point_crossover)

