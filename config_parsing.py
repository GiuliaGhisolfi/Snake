#configuration and log files paths
greedy_fold = './greedy_data/'
greedy_configs = [
    greedy_fold+'bot1.config', 
    greedy_fold+'bot2.config', 
    greedy_fold+'bot3.config',
    greedy_fold+'bot4.config',
    greedy_fold+'bot5.config',
    greedy_fold+'bot6.config',
    greedy_fold+'bot7.config'
    ]
greedy_logs = [
    greedy_fold+'log1.json', 
    greedy_fold+'log2.json', 
    greedy_fold+'log3.json',
    greedy_fold+'log4.json',
    greedy_fold+'log5.json',
    greedy_fold+'log6.json',
    greedy_fold+'log7.json'
    ]

hamilton_fold = './hamilton_data/'
hamilton_configs = [
    hamilton_fold+'bot1.config', 
    hamilton_fold+'bot2.config', 
    hamilton_fold+'bot3.config',
    hamilton_fold+'bot4.config',
    hamilton_fold+'bot5.config',
    hamilton_fold+'bot6.config',
    hamilton_fold+'bot7.config',
    hamilton_fold+'bot8.config',
    hamilton_fold+'bot9.config',
    hamilton_fold+'bot10.config',
    hamilton_fold+'bot11.config'
    ]
ham_logs = [
    hamilton_fold+'log1.json', 
    hamilton_fold+'log2.json', 
    hamilton_fold+'log3.json',
    hamilton_fold+'log4.json',
    hamilton_fold+'log5.json',
    hamilton_fold+'log6.json',
    hamilton_fold+'log7.json',
    hamilton_fold+'log8.json',
    hamilton_fold+'log9.json',
    hamilton_fold+'log10.json',
    hamilton_fold+'log11.json'
    ]

def read_config_file(file):
    param = {}
    with open(file, 'r') as c:
        for i, line in enumerate(c):
            if line.startswith('#') or len(line) == 1:  #check for informationless rows
                continue
            else:
                try:
                    #read params
                    sl = line.replace('\n', '').replace(' ', '').split('=')
                    param[sl[0]] = sl[1]
                except:
                    print('errore file config linea: ' + str(i))
    return param

def get_game_config(file):
    param = read_config_file(file)

    #sets params
    try:
        size = int(param['size'])
        x_blocks = int(param['x_blocks'])
        y_blocks = int(param['y_blocks'])
        frame_delay = int(param['frame_delay'])
        obstacles = str(param['obstacles']) 
        autostart = bool(param['autostart'])
        executions = int(param['executions'])
    except Exception as e:
        print(e)
        print('parameter value error')
        print('initialization with default values')
        size = 700
        x_blocks = 10
        y_blocks = 11
        frame_delay = 1
        obstacles = 'None'
        autostart = True
        executions = 30
    config_params = [size, x_blocks, y_blocks, frame_delay, obstacles, autostart, executions]
    return config_params