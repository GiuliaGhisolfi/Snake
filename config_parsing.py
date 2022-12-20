def read_config_file(file):
    param = {}
    with open(file, 'r') as c:
        for i, line in enumerate(c):
            if line.startswith('#') or len(line) == 1:
                continue
            else:
                try:
                    sl = line.replace('\n', '').replace(' ', '').split('=')
                    param[sl[0]] = sl[1]
                except:
                    print('errore file config linea: ' + str(i))
    return param

def get_game_config(file):
    param = read_config_file(file)
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
    return size, x_blocks, y_blocks, frame_delay, obstacles, autostart, executions