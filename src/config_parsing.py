def read_config_file(file):
    """Read and parse the configuration file."""
    param = {}
    with open(file, 'r') as c:
        for i, line in enumerate(c):
            if line.startswith('#') or len(line) == 1: # informationless row
                continue
            try:
                sl = line.replace('\n', '').replace(' ', '').split('=')
                param[sl[0]] = sl[1]
            except:
                print('errore file config linea: ' + str(i))
    return param

def get_game_config(file):
    """Return the configuration values."""
    param = read_config_file(file)
    try:
        param['grid_size'] = int(param['grid_size'])
        param['grid_width'] = int(param['grid_width'])
        param['grid_height'] = int(param['grid_height'])
        param['frame_delay'] = int(param['frame_delay'])
        param['obstacles'] = str(param['obstacles'])
        param['autostart'] = bool(param['autostart'])
        param['max_executions'] = int(param['max_executions'])
    except Exception as e:
        print(e)
        print('parameter value error')
        print('initialization with default values')
        param['grid_size'] = 700
        param['grid_width'] = 10
        param['grid_height'] = 11
        param['frame_delay'] = 1
        param['obstacles'] = 'None'
        param['autostart'] = True
        param['max_executions'] = 30
    return param