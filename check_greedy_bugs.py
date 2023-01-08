# DA ELIMINARE POI
import json
import numpy as np
from results_processing.utilis_json import *

CONFIGURATIONS = 7

#greedy_fold = './greedy_results/10x10/'
#greedy_fold = './greedy_results/15x16/'
greedy_fold = './greedy_results/10x10 1000/'

#names = ['irene', 'giulia', 'gabriele', 'luca', 'giacomo']
#names = ['luca', 'giacomo']
names = ['giacomo']

data_greedy = []
errors = 0
for i in range(1, CONFIGURATIONS + 1):
    for name in names:
        data = []
        file = greedy_fold + name + '/log' + '%s'%i + '.json'
        f = open(file)
        data += json.load(f)

        for j in range(len(data)):
            if((data[j][-1][1] - data[j][-2][1] != 1) and (i != 1)):
                print("ERRORE!!!!")
                print("conf:" + str(i))
                print(name)
                print("ultimo step: " + str(data[j][-2][1]) + " -> " + str(data[j][-1][1]))
                print()
                errors += 1    

        f.close()
    data_greedy.append(data)

if(errors == 0) : print("nice! :)\nno errors out of configuration 1")
else: print("total errors: " + str(errors))
