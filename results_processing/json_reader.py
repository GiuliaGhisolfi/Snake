import json
import numpy as np
from utilis_json import *



def total_time_len(iterations_time, snake_length):
    total_time = np.sum(iterations_time)
    mean_time = np.mean(total_time, axis=0)
    std_time = np.std(total_time, axis=0)
    
    max_len = snake_length[:, -1]
    mean_len = np.mean(max_len, axis=0)
    std_len = np.std(max_len, axis=0)
    
    results.write("averege time to complite the game: %f [sec], std dev: %f \n" %(mean_time, std_len))
    results.write("average length achieved at the end of the game %f, std dev: %f : \n" %(mean_len, std_len))


greedy_fold = './greedy_results/'
hamilton_fold = './hamilton_results/'
names = ['irene', 'giulia', 'gabriele', 'luca', 'giacomo']
dimension = ['10x10']

FILE_RESULTS = './results_processing/results_10x10/results.txt'
results = open(FILE_RESULTS, 'w')


#------------------------------------------------------------------------------------------------------------
#------------------------------------------Read data from file json------------------------------------------
"""
Results:
data_strategy = [ [data config1], [data config2], ... ] 
strategy_config_k = [ [first game data for k-th strategy configuration], [second game], ... ]
[k-th game data] = [ [time to make first iteration, snake length during first iteration], ... ]
"""

#---------------------------------greedy----------------------------------
data_greedy = []
for i in range(1, 7+1):
    data = []
    dim = dimension[0]
    for name in names:
        file = greedy_fold+dim+'/'+name+'/log'+'%s'%i+'.json'
        f = open(file)
        data += json.load(f)
        f.close()
    data_greedy.append(data)

#---------------------------------hamilton---------------------------------
data_hamilton = []
for i in range(1, 11+1):
    data = []
    dim = dimension[0]
    for name in names:
        file = hamilton_fold+dim+'/'+name+'/log'+'%s'%i+'.json'
        f = open(file)
        data += json.load(f)
        f.close()
    data_hamilton.append(data)


#-----------------------------------------------------------------------------------------------------------
#----------------------------------------------Data processing----------------------------------------------

#---------------------------------greedy----------------------------------
fold = "./results_processing/results_10x10/greedy/"
strategy = "greedy"
data_greedy_time_average = []
data_greedy_time_std = []
data_greedy_length_average = []
data_greedy_length_std = []
games_won_total = [] # games won out of total for each config

results.write('GREEDY \n')

for i in range(1, 7+1):
    # Divido i dati di greedy in due matrici, una con i giochi vinti e una con quelli persi per ogni configurazione 
    # e salvo il rapporto dei giochi vinti
    games_won_data, games_lost_data, games_won = divides_games_won_lost(data_greedy[i-1])
    games_won_total.append(games_won)
    print('percentage of games won out of total for greedy configuration %d = %f' %(i, games_won*100) )

    # trascrizione dati e grafici
    results.write('greedy config %s \n' % i)

    iterations_time, snake_length = split_iteration_length_data(data_greedy[i-1])
    plot_single_config(iterations_time, snake_length, i, fold, strategy)
    
    total_time_len(iterations_time, snake_length)
    results.write('Percentage of games won out of total = %f \n' %games_won*100)
    results.write('Games won \n')
    total_time_len( split_iteration_length_data(games_won_data) )
    results.write('Games lost \n')
    total_time_len( split_iteration_length_data(games_lost_data) )
    results.write('\n')
    
    # media e dev std tempo per iterazione
    time_for_iterartion_averege, time_for_iterartion_std = calculate_averege_std(iterations_time)
    data_greedy_time_average.append(time_for_iterartion_averege)
    data_greedy_time_std.append(time_for_iterartion_std)
    
    # media e dev std lunghezza snake ad ogni iterazione
    len_for_iterartion_averege, len_for_iterartion_std = calculate_averege_std(iterations_time)
    data_greedy_length_average.append(len_for_iterartion_averege)
    data_greedy_length_std.append(len_for_iterartion_std)

plot_iterations_time_different_config(data_greedy_time_average, data_greedy_time_std, fold, strategy)
plot_iterations_lenght_snake_different_config(data_greedy_length_average, data_greedy_length_std, fold, strategy)
plot_violin(data_greedy_time_average, fold, 'Time', strategy)
plot_violin(data_greedy_length_average, fold, 'Length', strategy)


#---------------------------------hamilton---------------------------------
fold = "./results_processing/results_10x10/hamilton/"
strategy = "hamilton"
data_hamilton_time_average = []
data_hamilton_time_std = []
data_hamilton_length_average = []
data_hamilton_length_std = []

results.write('\n\n')
results.write('HAMILTON \n')

for i in range(1, 11+1):
    # tolgo step finale di controllo da ogni gioco
    data_hamilton[i-1], _, games_won = divides_games_won_lost(data_hamilton[i-1])
    if games_won != 1:
        print('percentage of games won out of total for hamilton configuration %d = %f' %(i, games_won*100))

    # trascrizione dati e grafici
    results.write('hamilton config %s \n' % i)
    
    iterations_time, snake_length = split_iteration_length_data(data_hamilton[i-1])
    plot_single_config(iterations_time, snake_length, i, fold, strategy)
    
    total_time_len(iterations_time, snake_length)

    # media e dev std tempo per iterazione
    time_for_iterartion_averege, time_for_iterartion_std = calculate_averege_std(data_hamilton[i-1])
    data_hamilton_time_average.append(time_for_iterartion_averege)
    data_hamilton_time_std.append(time_for_iterartion_std)

    # media e dev std lunghezza snake ad ogni iterazione
    len_for_iterartion_averege, len_for_iterartion_std = calculate_averege_std(iterations_time)
    data_hamilton_length_average.append(len_for_iterartion_averege)
    data_hamilton_length_std.append(len_for_iterartion_std)

plot_iterations_time_different_config(data_hamilton_time_average, data_hamilton_time_std, fold, strategy)
plot_iterations_lenght_snake_different_config(data_hamilton_length_average, data_hamilton_length_std, fold, strategy)
plot_violin(data_hamilton_time_average, fold, 'Time', strategy)
plot_violin(data_hamilton_length_average, fold, 'Length', strategy)
