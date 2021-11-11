import random
import itertools

numberOfActions=200
cleaningSessions=100
somelists=[[0,1,2] for i in range(5)] 
perceptions= [list(element) for element in itertools.product(*somelists)]
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
