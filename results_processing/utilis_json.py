import matplotlib.pyplot as plt
import numpy as np

names = ['irene', 'giulia', 'gabriele', 'luca', 'giacomo']

#-------------DATA PROCESSING-------------

def split_iteration_length_data(data):
    """divide i dati in due matrici, una per i tempi e una la lunghezza dello snake"""
    iterations_time = []  # iterations_time = [ [tempi primo gioco], [secondo], ... ]
    snake_length = []  # snake_length = [ [lung. primo gioco], [secondo], ... ]

    for game in data:
        temporary_iter = []
        temporary_length = []
        for element in game:
            temporary_iter.append(element[0])
            temporary_length.append(element[1])
        iterations_time.append(temporary_iter)
        snake_length.append(temporary_length)

    return iterations_time, snake_length

def plot_single_config(iterations_time, snake_length, i, fold, strategy):
    plot_iterations_time(iterations_time, i, fold, strategy)
    plot_iterations_length(snake_length, i, fold, strategy)
    plot_time_length(iterations_time, snake_length, i, fold, strategy)
    

def calculate_averege_std(data):
    """ritorna: time_for_iterartion_averege = [ tempo medio prime iterzioni, seconde iter, ... ]
                time_for_iterartion_std = [deviazione standard prime iter, seconde iter, ... ]
                per la configurazone di cui abbiamo dato i dati in input"""

    #data = [ [first game iterations time ], [second game], ... ]
    data = np.array(data)
    max_iter = max(len(game) for game in data)
    for j in range(len(data)):
        len_game = len(data[j])
        for _ in range(max_iter - len_game):
            data[j].append(0)

    time_for_iterartion_averege = []
    time_for_iterartion_std = []
    for l in range(len(data[0])):
        iteration_data = []
        for game in data:
            if game[l] != 0:
                iteration_data.append(game[l])
        time_for_iterartion_averege.append( np.average(iteration_data) )
        time_for_iterartion_std.append( np.std(iteration_data) )

    return time_for_iterartion_averege, time_for_iterartion_std

def divides_games_won_lost(data, grid_area=10*10):
    """ritorna: 
    games_won_data = [ [first game won data for k-th strategy configuration], [second game], ... ]
    games_lost_data = [ [first game lost data for k-th strategy configuration], [second game], ... ]
    games_won := rapporto partite vinte su totale partite per configurazione k-esima
    games_lost := raport partite perse
    """
    games_won_data = []
    games_lost_data = []
    
    for game in data:
        if game[-1] == [0, grid_area]:
            game.pop(-1)
            games_won_data.append(game)
        else:
            games_lost_data.append(game)

    games_won = len(games_won_data) / len(data)

    return games_won_data, games_lost_data, games_won


#------------------PLOT------------------

def plot_iterations_time(iterations_time, i, fold, strategy):
    """asse x: numero iterazione, asse y: tempo dall'inizio del gioco"""
    rep = 1000
    colors = plt.cm.get_cmap("tab10")
    plt.figure()
    for c, game in enumerate(iterations_time):
        time_sum = 0
        y_vectore = []
        for l in range(len(game)):
            time_sum += game[l]
            y_vectore.append(time_sum)
        x_vectore = np.linspace(1, len(y_vectore), len(y_vectore))
        if c%rep==0:
            plt.semilogy(x_vectore, y_vectore, linewidth=0.8, color=colors(int(c/rep)), label=names[int(c/rep)])
        else:
            plt.semilogy(x_vectore, y_vectore, linewidth=0.8, color=colors(int(c/rep)))
    plt.xlabel("game step")
    plt.ylabel("log(time [sec])")
    plt.title('%s config%d' %(strategy, i))
    plt.grid()
    plt.legend()
    plt.savefig(fold+"config{}_iterations_time.pdf".format(i), bbox_inches="tight")
    
def plot_iterations_length(iterations_length, i, fold, strategy):
    """asse x: numero iterazione, asse y: lunghezza dello snake"""
    plt.figure()
    for game in iterations_length:
        x_vectore = np.linspace(1, len(game), len(game))
        plt.plot(x_vectore, game, linewidth=0.8)
    plt.xlabel("game step")
    plt.ylabel("snake length")
    plt.title('%s config%d' %(strategy, i))
    plt.grid()
    plt.savefig(fold+"config{}_iterations_length.pdf".format(i), bbox_inches="tight")
    
def plot_time_length(iterations_time, iterations_length, i, fold, strategy):
    """asse x: tempo dall'inizio del gioco, asse y: lunghezza dello snake"""
    colors = plt.cm.get_cmap("tab10")
    plt.figure()
    j = 0
    rep = 1000
    for c, game in enumerate(iterations_time):
        time_sum = 0
        x_vectore = []
        for l in range(len(game)):
            time_sum += game[l]
            x_vectore.append(time_sum)
        y_vectore = iterations_length[j]
        j += 1
        if c%20==0:
            plt.plot(x_vectore, y_vectore, linewidth=0.8, color=colors(int(c/rep)), label=names[int(c/rep)])
        else:
            plt.plot(x_vectore, y_vectore, linewidth=0.8, color=colors(int(c/rep)))

    plt.xlabel("time [sec]")
    plt.ylabel("snake length")
    plt.title('%s config%d' %(strategy, i))
    plt.grid()
    plt.legend()
    plt.savefig(fold+"config{}_time_length.pdf".format(i), bbox_inches="tight")
    
def plot_iterations_time_different_config(averege_time, std_time, fold, strategy):
    plt.figure()
    colors = plt.cm.get_cmap("tab10")
    #color = ['r', 'b', 'g', 'm', 'c', 'y', 'purple', 'orange', 'olive', 'pink', 'red']
    i = 0
    for aver, std in zip(averege_time, std_time):
        y_vector = []
        sum = 0
        
        x_vectore = np.linspace(1, len(aver), len(aver))
        for t in aver:
            sum += t
            y_vector.append(sum)

        std = np.array(std)
        if i==10:
            plt.semilogy(x_vectore, y_vector, label="config{}".format(i+1), linewidth=0.8, color='black')
        else:
            plt.semilogy(x_vectore, y_vector, label="config{}".format(i+1), linewidth=0.8, color=colors(i))
        #plt.semilogy(x_vectore, y_vector+std, alpha=0.2, color=color[i], linewidth=0.5)
        #plt.semilogy(x_vectore, y_vector-std, alpha=0.2, color=color[i], linewidth=0.5)
        i += 1
        
    plt.legend()
    plt.xlabel("game step")
    plt.ylabel("log(time [sec])")
    #plt.title("Averege and stadard deviation of time for each %s configuration" % strategy)
    plt.title("Averege of time for each %s configuration" % strategy)
    plt.grid()
    plt.savefig(fold+"all_config_averege_time.pdf", bbox_inches="tight")
    
def plot_iterations_lenght_snake_different_config(averege_length, std_length, fold, strategy):
    plt.figure()
    colors = plt.cm.get_cmap("tab10")
    #color = ['r', 'b', 'g', 'm', 'c', 'y', 'purple', 'orange', 'olive', 'pink', 'red']
    i = 0
    for aver, std in zip(averege_length, std_length):
        aver = np.array(aver)
        std = np.array(std)
        x_vectore = np.linspace(1, len(aver), len(aver))
        if i==10:
            plt.plot(x_vectore, aver, label="config{}".format(i+1), linewidth=0.8, color='black')
        else:
            plt.plot(x_vectore, aver, label="config{}".format(i+1), linewidth=0.8, color=colors(i))
        #plt.plot(x_vectore, aver+std, alpha=0.2, color=color[i], linewidth=0.5)
        #plt.plot(x_vectore, aver+std, alpha=0.2, color=color[i], linewidth=0.5)
        i += 1
        
    plt.legend()
    plt.xlabel("game step")
    plt.ylabel("snake length")
    plt.grid()
    #plt.title("Averege and stadard deviation of snake length for each %s configuration" % strategy)
    plt.title("Averege of snake length for each %s configuration" % strategy)
    plt.savefig(fold+"all_config_averege_length.pdf", bbox_inches="tight")

def plot_violin(iterations_time, fold, name, strategy, ylbl):
    plt.figure(figsize=(10.4, 4.8))
    plt.violinplot(iterations_time)
    if ylbl=='time':
        plt.ylabel("time [sec]")
    else:
        plt.ylabel("snake length")
    plt.grid()
    plt.title('%s' %(strategy))

    if strategy=='Greedy': n_configs = 7
    else: n_configs = 11
    configs_names = []
    configs_idx = []
    for c in range(n_configs):
        configs_names.append('config%d'%(c+1))
        configs_idx.append(c+1)
    plt.xticks(configs_idx, configs_names)
    
    plt.savefig(fold+"%s_violinplot.pdf" % name, bbox_inches="tight")