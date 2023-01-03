import matplotlib.pyplot as plt
import numpy as np

#-------------DATA PROCESSING-------------

def split_iteration_length_data(data, i):
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

    #plot_iterations_time(iterations_time, i)
    plot_iterations_length(snake_length, i)
    return iterations_time, snake_length

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

def plot_iterations_time(iterations_time, i):
    """asse x: numero iterazione, asse y: tempo dall'inizio del gioco"""
    plt.figure()
    for game in iterations_time:
        time_sum = 0
        y_vectore = []
        for l in range(len(game)):
            time_sum += game[l]
            y_vectore.append(time_sum)
        x_vectore = np.linspace(1, len(y_vectore), len(y_vectore))
        plt.plot(x_vectore, y_vectore, linewidth=0.5)
    plt.xlabel("k-th iteration")
    plt.ylabel("time [sec]")
    plt.grid()
    plt.savefig("./hamilton_plot/ham_config{}_iterations_time".format(i))
    
def plot_iterations_length(iterations_length, i):
    """asse x: numero iterazione, asse y: lunghezza dello snake"""
    plt.figure()
    for game in iterations_length:
        x_vectore = np.linspace(1, len(game), len(game))
        plt.plot(x_vectore, game, linewidth=0.5)
    plt.xlabel("k-th iteration")
    plt.ylabel("snake length")
    plt.grid()
    plt.savefig("./hamilton_plot/ham_config{}_iterations_length".format(i))
    
def plot_iterations_time_different_config(averege_time, std_time):
    plt.figure()
    color = ['r', 'b', 'g', 'm', 'c', 'y', 'purple', 'orange', 'olive', 'pink', 'red']
    i = 0
    for aver, std in zip(averege_time, std_time):
        x_vectore = np.linspace(1, len(aver), len(aver))
        aver = np.array(aver)
        std = np.array(std)
        plt.semilogy(x_vectore, aver, label="config{}".format(i+1), color=color[i], linewidth=0.5)
        plt.semilogy(x_vectore, aver+std, alpha=0.2, color=color[i], linewidth=0.5)
        plt.semilogy(x_vectore, aver-std, alpha=0.2, color=color[i], linewidth=0.5)
        i += 1
        
    plt.legend()
    plt.xlabel("k-th iteration")
    plt.ylabel("log(time [sec])")
    plt.title("Averege and stadard deviation of time for every configuration")
    plt.savefig("./hamilton_plot/ham_all_config_averege_std_time")
    
def plot_iterations_lenght_snake_different_config(averege_length, std_length):
    plt.figure()
    color = ['r', 'b', 'g', 'm', 'c', 'y', 'purple', 'orange', 'olive', 'pink', 'red']
    i = 0
    for aver, std in zip(averege_length, std_length):
        aver = np.array(aver)
        std = np.array(std)
        x_vectore = np.linspace(1, len(aver), len(aver))
        plt.plot(x_vectore, aver, label="config{}".format(i+1), color=color[i], linewidth=0.5)
        plt.plot(x_vectore, aver+std, alpha=0.2, color=color[i], linewidth=0.5)
        plt.plot(x_vectore, aver+std, alpha=0.2, color=color[i], linewidth=0.5)
        i += 1
        
    plt.legend()
    plt.xlabel("k-th iteration")
    plt.ylabel("snake length")
    plt.title("Averege and stadard deviation of snake length for every configuration")
    plt.savefig("./hamilton_plot/ham_all_config_averege_std_length")
        
def plot_violin(iterations_time):
    plt.figure()
    plt.violinplot(iterations_time)
    plt.xlabel("configuration")
    plt.ylabel("time [sec]")
    plt.savefig("./hamilton_plot/ham_all_config_violinplot")