from program import defaultMutation,random,np,run,itertools
from mutation import swapMutation

def divide_chunks(l, n):
    """
    Yield successive n-sized
    chunks from l.
    Taken from: https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    """    
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def multipleCrossover(father,mother,mutationFunction=defaultMutation):
    genY,genX = father,mother
    nOfslices=random.randint(2,6)
    genYWithSlices = list(divide_chunks(genY,nOfslices))
    genXWithSlices = list(divide_chunks(genX,nOfslices))
    children=[[],[]]
    for i in range(len(genXWithSlices)):
        if i%2==0:
            children[0]+=genXWithSlices[i]
            children[1]+=genYWithSlices[i]
        else:
            children[0]+=genYWithSlices[i]
            children[1]+=genXWithSlices[i]
    children=mutationFunction(children)
    return children



if __name__ == '__main__':
    f = open("generationDataWithMultipleCrossover.csv","w")
    somelists=[[0,1,2] for i in range(5)] 
    perceptions= [list(element) for element in itertools.product(*somelists)]
    run(f,perceptions,mutationFunction=swapMutation,mate=multipleCrossover)