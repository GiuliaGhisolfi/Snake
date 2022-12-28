#configuration and log files paths
greedy_configs_fold = './greedy_configs/'
greedy_configs = [
    greedy_configs_fold+'bot1.config', 
    greedy_configs_fold+'bot2.config', 
    greedy_configs_fold+'bot3.config',
    greedy_configs_fold+'bot4.config',
    greedy_configs_fold+'bot5.config',
    greedy_configs_fold+'bot6.config',
    greedy_configs_fold+'bot7.config'
    ]
greedy_results_fold = './greedy_results/'
greedy_logs = [
    greedy_results_fold+'log1.json', 
    greedy_results_fold+'log2.json', 
    greedy_results_fold+'log3.json',
    greedy_results_fold+'log4.json',
    greedy_results_fold+'log5.json',
    greedy_results_fold+'log6.json',
    greedy_results_fold+'log7.json'
    ]

hamilton_configs_fold = './hamilton_configs/'
hamilton_configs = [
    hamilton_configs_fold+'bot1.config', 
    hamilton_configs_fold+'bot2.config', 
    hamilton_configs_fold+'bot3.config',
    hamilton_configs_fold+'bot4.config',
    hamilton_configs_fold+'bot5.config',
    hamilton_configs_fold+'bot6.config',
    hamilton_configs_fold+'bot7.config',
    hamilton_configs_fold+'bot8.config',
    hamilton_configs_fold+'bot9.config',
    hamilton_configs_fold+'bot10.config',
    hamilton_configs_fold+'bot11.config'
    ]
hamilton_results_fold = './hamilton_results/'
ham_logs = [
    hamilton_results_fold+'log1.json', 
    hamilton_results_fold+'log2.json', 
    hamilton_results_fold+'log3.json',
    hamilton_results_fold+'log4.json',
    hamilton_results_fold+'log5.json',
    hamilton_results_fold+'log6.json',
    hamilton_results_fold+'log7.json',
    hamilton_results_fold+'log8.json',
    hamilton_results_fold+'log9.json',
    hamilton_results_fold+'log10.json',
    hamilton_results_fold+'log11.json'
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
        param['size'] = int(param['size'])
        param['x_blocks'] = int(param['x_blocks'])
        param['y_blocks'] = int(param['y_blocks'])
        param['frame_delay'] = int(param['frame_delay'])
        param['obstacles'] = str(param['obstacles']) 
        param['autostart'] = bool(param['autostart'])
        param['executions'] = int(param['executions'])
    except Exception as e:
        print(e)
        print('parameter value error')
        print('initialization with default values')
        param['size'] = 700
        param['x_blocks'] = 10
        param['y_blocks'] = 11
        param['frame_delay'] = 1
        param['obstacles'] = 'None'
        param['autostart'] = True
        param['executions'] = 30
    return param