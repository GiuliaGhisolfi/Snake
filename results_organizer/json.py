import json
import numpy as np

greedy_fold = './greedy_results/'
hamilton_fold = './hamilton_results/'
names = ['irene', 'giulia']


#greedy
for i in range(1, 7+1):
    data = []
    for name in names:
        file = greedy_fold+name+'/log'+'%s'%i+'.json'
        f = open(file)
        data += json.load(f)
        f.close()
    globals()['greedy_config%s' % i] = data
    
#hamilton
for i in range(1, 11+1):
    data = []
    for name in names:
        file = hamilton_fold+name+'/log'+'%s'%i+'.json'
        f = open(file)
        data += json.load(f)
        f.close()
    globals()['hamilton_config%s' % i] = data
    