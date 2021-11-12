import random
import itertools
import program

def removePerceptions(perceptions):
    i=0
    new_p = list()
    while i<len(perceptions):
        c = 0
        for status in perceptions[i]:
            if status == 2:
                c = c + 1
                if c > 2 or perceptions[i][4] == 2:
                    new_p.append(perceptions[i])
        i=i+1

    for p in new_p:
        if p in perceptions:
            perceptions.remove(p) 
    return perceptions
    #aló PoLiSíA



if __name__=="__main__":
    f = open("dataGenerationWithReduction.csv","w")
    somelists=[[0,1,2] for i in range(5)] 
    perceptions= [list(element) for element in itertools.product(*somelists)]
    perceptions = removePerceptions(perceptions)
    program.run(f,perceptions)