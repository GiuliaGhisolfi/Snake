import json
import numpy as np
from utilis_json import *

greedy_fold = './greedy_results/'
hamilton_fold = './hamilton_results/'
#names = ['irene', 'giulia', 'gabriele', 'luca']
names = ['gabriele']


#---------Read data from file json---------
"""
Results:   
strategy_config_k = [ [first game data for k-th strategy configuration], [second game], ... ]
[k-th game data] = [ [time to make first iteration, snake length during first iteration], ... ]
"""

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

#------------Data processing------------

games_won_total = [] # games won out of total for each config
for i in range(1, 7+1):
    # Divido i dati di greedy in due matrici, una con i giochi vinti e una con quelli persi per ogni configurazione 
    # e salvo il rapporto dei giochi vinti
    
    games_won_data, games_lost_data, games_won = divides_games_won_lost(globals()['greedy_config%s' % i])
    globals()['greedy_config%s_won' % i] = games_won_data
    globals()['greedy_config%s_lost' % i] = games_lost_data
    games_won_total.append(games_won)
    print('percentage of games won out of total for greedy configuration %d = %f' %(i, games_won*100) )

for i in range(1, 11+1):
    games_won_data, games_lost_data, games_won = divides_games_won_lost(globals()['hamilton_config%s' % i])
    globals()['hamilton_config%s' % i] = games_won_data
    if games_won != 1:
        print('percentage of games won out of total for hamilton configuration %d = %f' %(i, games_won*100) )

# TODO: ho tutti i dati, adesso fare i grafici :) -> guarda funzioni in utils_json