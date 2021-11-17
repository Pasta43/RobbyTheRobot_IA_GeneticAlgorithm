from reduccion import random,itertools,program,removePerceptions
def mutation(children):
    c = 0
    for j in range(len(children[0])):
        if children[0][j] == children[1][j]:
            c += 1
    if c / 243 > 0.7:
        modifications= random.randint(1,20)
        for i in range(modifications):
            children[0][random.randint(0,len(children[0])-1)]=random.randint(0,6)
            children[1][random.randint(0,len(children[1])-1)]=random.randint(0,6)
    return children

if __name__ == "__main__":
    f = open("dataGenerationWithSimilarity.csv","w")
    somelists=[[0,1,2] for i in range(5)] 
    perceptions= [list(element) for element in itertools.product(*somelists)]
    perceptions = removePerceptions(perceptions)
    program.run(f,perceptions,mutation)