from reduccion import removePerceptions, itertools, program,random
def virus(children):
    if (random.random()<0.05):
        size= random.randint(0,len(children[0])//4)
        viruses = [random.randint(0,6) for _ in range(size)]
        randomValue=random.randint(0,len(children[0])//2)
        children[0][randomValue:randomValue+size]=viruses
        children[1][randomValue:randomValue+size]=viruses
    return children
if __name__=="__main__":
    f = open("dataGenerationWithVirus.csv","w")
    somelists=[[0,1,2] for i in range(5)] 
    perceptions= [list(element) for element in itertools.product(*somelists)]
    perceptions = removePerceptions(perceptions)
    program.run(f,perceptions,virus)