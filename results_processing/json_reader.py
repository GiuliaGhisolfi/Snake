import json
import numpy as np
from utilis_json import *

def total_time_len(iterations_time, snake_length):
    total_time = []
    for game in iterations_time:
        total_time.append( np.sum(game, axis=0) )
    mean_time = np.mean(total_time, axis=0)
    std_time = np.std(total_time, axis=0)
    
    total_iteration_number = []
    for game in iterations_time:
        total_iteration_number.append( len(game))
    mean_iter = np.mean(total_iteration_number, axis=0)
    std_iter = np.std(total_iteration_number, axis=0)
    
    max_len = []
    for game in snake_length:
        max_len.append(game[-1])
    mean_len = np.mean(max_len, axis=0)
    std_len = np.std(max_len, axis=0)
    
    results.write("Averege time to complete the game: %f [sec], std dev: %f [sec] \n" %(mean_time, std_time))
    results.write("Averege number of iteration to complite the game: %f [iterations], std dev: %f [iterations] \n" %(mean_iter, std_iter))
    results.write("Average length achieved at the end of the game %f, std dev: %f \n" %(mean_len, std_len))


greedy_fold = './greedy_results/'
hamilton_fold = './hamilton_results/'
names = ['irene', 'giulia', 'gabriele', 'luca', 'giacomo']
names2 = ['giacomo']
# TODO: 
# irene => 1,6 GHz Intel Core i5
# giulia => Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz   1.80 GHz
# gabriele => Apple M1 Pro 2.064 GHz / 3.228 GHz
# luca => Intel® Core™ i7-7500U CPU @ 2.70GHz × 4
# giacomo => Intel Core i7-10750H CPU @ 2.60GHz
dimension = ['10x10']
dimension2 = ['10x10 1000']

FILE_RESULTS = './results_processing/results_10x10/results.csv'
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
for i in range(1, 10+1):
    data = []
    dim = dimension2[0]
    for name in names2:
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
strategy = "Greedy"
data_greedy_time_average = []
data_greedy_time_std = []
data_greedy_length_average = []
data_greedy_length_std = []
data_greedy_total_time = []
games_won_total = [] # games won out of total for each config

results.write('GREEDY \n')
ratio = []
for i in range(1, 10+1):
    # Divido i dati di greedy in due matrici, una con i giochi vinti e una con quelli persi per ogni configurazione 
    # e salvo il rapporto dei giochi vinti
    games_won_data, games_lost_data, games_won = divides_games_won_lost(data_greedy[i-1])
    games_won_total.append(games_won)
    print('Ratio of games won out of total for greedy configuration %d = %f' % (i, games_won) )

    # trascrizione dati e grafici
    results.write('\nGreedy config %s \n' % i)

    iterations_time, snake_length = split_iteration_length_data(data_greedy[i-1])
    plot_single_config(iterations_time, snake_length, i, fold, strategy)
    
    tot_time = []
    for game in iterations_time:
        tot_time.append( np.sum(game, axis=0) )
    data_greedy_total_time.append(tot_time)
    
    iterations_time_won, snake_length_won = split_iteration_length_data(games_won_data)
    iterations_time_lost, snake_length_lost = split_iteration_length_data(games_lost_data)
    
    for game in snake_length_won:
        game[-1] += 1 # se vince lunghezza finale == grid area

    snake_length_tot = []
    snake_length_tot += snake_length_won
    snake_length_tot += snake_length_lost
    
    total_time_len(iterations_time, snake_length_tot)
    results.write('Ratio of games won out of total = %f \n' %games_won)
    ratio.append(games_won)
    results.write('Games won: \n')
    total_time_len(iterations_time_won, snake_length_won)
    results.write('Games lost: \n')
    total_time_len( iterations_time_lost, snake_length_lost )
    
    # media e dev std tempo per iterazione
    time_for_iterartion_averege, time_for_iterartion_std = calculate_averege_std(iterations_time)
    data_greedy_time_average.append(time_for_iterartion_averege)
    data_greedy_time_std.append(time_for_iterartion_std)
    
    # media e dev std lunghezza snake ad ogni iterazione
    len_for_iterartion_averege, len_for_iterartion_std = calculate_averege_std(snake_length)
    data_greedy_length_average.append(len_for_iterartion_averege)
    data_greedy_length_std.append(len_for_iterartion_std)

plot_iterations_time_different_config(data_greedy_time_average, data_greedy_time_std, fold, strategy)
plot_iterations_lenght_snake_different_config(data_greedy_length_average, data_greedy_length_std, fold, strategy)
plot_violin(data_greedy_time_average, None, fold, 'Time_per_iteration', strategy, 'time')
plot_violin(data_greedy_length_average, None, fold, 'Length_per_iteration', strategy, 'length')
plot_violin(data_greedy_total_time, ratio, fold, 'Game_time', strategy, 'time')


#---------------------------------hamilton---------------------------------
fold = "./results_processing/results_10x10/hamilton/"
strategy = "Hamilton"
data_hamilton_time_average = []
data_hamilton_time_std = []
data_hamilton_length_average = []
data_hamilton_length_std = []
data_hamilton_total_time = []

results.write('\n\n')
results.write('HAMILTON \n')

for i in range(1, 11+1):
    # tolgo step finale di controllo da ogni gioco
    data_hamilton[i-1], _, games_won = divides_games_won_lost(data_hamilton[i-1])
    if games_won != 1:
        print('Ratio of games won out of total for hamilton configuration %d = %f' %(i, games_won))

    # trascrizione dati e grafici
    results.write('\nHamilton config %s \n' % i)
    
    iterations_time, snake_length = split_iteration_length_data(data_hamilton[i-1])
    plot_single_config(iterations_time, snake_length, i, fold, strategy)
    
    tot_time = []
    for game in iterations_time:
        tot_time.append( np.sum(game, axis=0) )
    data_hamilton_total_time.append(tot_time)
    
    for game in snake_length:
        game[-1] += 1
    total_time_len(iterations_time, snake_length)

    # media e dev std tempo per iterazione
    time_for_iterartion_averege, time_for_iterartion_std = calculate_averege_std(iterations_time)
    data_hamilton_time_average.append(time_for_iterartion_averege)
    data_hamilton_time_std.append(time_for_iterartion_std)

    # media e dev std lunghezza snake ad ogni iterazione
    len_for_iterartion_averege, len_for_iterartion_std = calculate_averege_std(snake_length)
    data_hamilton_length_average.append(len_for_iterartion_averege)
    data_hamilton_length_std.append(len_for_iterartion_std)

plot_iterations_time_different_config(data_hamilton_time_average, data_hamilton_time_std, fold, strategy)
plot_iterations_lenght_snake_different_config(data_hamilton_length_average, data_hamilton_length_std, fold, strategy)
plot_violin(data_hamilton_time_average, None, fold, 'Time_per_iteration', strategy, 'time')
plot_violin(data_hamilton_length_average, None, fold, 'Length_per_iteration', strategy, 'length')
plot_violin(data_hamilton_total_time, None, fold, 'Game_time', strategy, 'time')

results.close()