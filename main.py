import pygame, sys
import numpy as np
from grid import Grid
from human_player import HumanPlayer
from bot_greedy import Bot_greedy
from bot_hamilton import Bot_hamilton
from bot_blind import Bot_blind
from bot_random import Bot_random
from snake import Snake
from food import Food
from config_parsing import *
import gui
import colors

TEST_MODE = True

def start(params):
    # parameters initialization
    size = params['size']
    x_blocks = params['x_blocks']
    y_blocks = params['y_blocks']
    frame_delay = params['frame_delay']
    obstacles = params['obstacles']
    autostart = params['autostart']
    max_executions = params['executions']
    player_info = params['player_info']
    bot_config = params['bot_config']
    log_file = params['log_file']

    grid = Grid(size, x_blocks, y_blocks)

    # create the window for the game
    if not TEST_MODE:
        pygame.init()
        gui.window = pygame.display.set_mode(grid.bounds)
        pygame.display.set_caption('Snake')
        grid.update_grid_dimensions(x_blocks, y_blocks) # non serve cambiarla in test mode perché per ogni execution
                                                        # le dimensioni rimangono sempre le stesse (quelle scritte nel file di config)

    # create snake, obstacles and food
    snake = Snake(color = player_info['color'], start_location = player_info['start_location'])
    snake.respawn(grid)
    grid.spawn_obstacles(obstacles)
    food = Food(colors.RED)
    food.respawn(snake, grid)

    # bot selection
    if player_info['type'] == 'human':
        player = HumanPlayer(
            game = pygame,
            up_key = pygame.K_UP,
            down_key = pygame.K_DOWN,
            right_key = pygame.K_RIGHT,
            left_key = pygame.K_LEFT)
    elif player_info['type'] == 'greedy':
        player = Bot_greedy(grid, snake, food, bot_config, log_file)
    elif player_info['type'] == 'hamilton':
        player = Bot_hamilton(grid, snake, food, bot_config, log_file, obstacles)
    elif player_info['type'] == 'blind':
        player = Bot_blind(grid, snake, food)
    elif player_info['type'] == 'random':
        player = Bot_random(grid, snake, food)
    else:
        print('PLAYERS INFO ERROR: player type not recognized')
        exit(1)

    executions = 0
    while (executions < max_executions) and (executions < sys.maxsize): # così non va in overflow, ed è plausibile che l'utente non voglia fare più 9*(10^18) esecuzioni di fila
        if not TEST_MODE:
            pygame.time.delay(frame_delay)
            # exit the game if the x button has been clicked
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    executions = max_executions

        # retrieve next move
        dir = player.get_next_move()
        
        
        # check if eaten
        eaten = snake.move(dir, food)
        
        # check if lose
        lost = snake.bounds_collision(grid) or snake.tail_collision()
        if lost:
            if TEST_MODE: 
                print('Execution %d/%d'%(executions+1, max_executions))
            else:
                text = gui.font.render('GAME OVER', True, colors.RED)
                gui.window.blit(text, (gui.window.get_size()[0]/3, gui.window.get_size()[1]/3))  
                pygame.display.update()
                pygame.time.delay(gui.DEATH_DELAY)
            
            executions += 1
            if player_info['type'] != 'human':
                player.save_data(executions==max_executions, lost)
            snake.respawn(grid)
            grid.spawn_obstacles(obstacles)
            food.respawn(snake, grid)
            if not autostart: gui.new_game() # con test mode è sempre autostart, lasciamo comunque così?
        elif snake.length == grid.get_grid_free_area(): # win
            if TEST_MODE: 
                print('Execution %d/%d'%(executions+1, max_executions))
            else:
                snake.draw(pygame, gui.window, grid)
                grid.draw_obstacles(pygame, gui.window)
                snake.draw(pygame, gui.window, grid)
                text = gui.font.render('COMPLETE', True, colors.RED)
                gui.window.blit(text, (gui.window.get_size()[0]/3, gui.window.get_size()[1]/2))
                pygame.display.update()
                pygame.time.delay(gui.DEATH_DELAY)
            
            executions += 1
            player.save_data(executions==max_executions, lost)
            snake.respawn(grid)
            grid.spawn_obstacles(obstacles)
            food.respawn(snake, grid)
            if not autostart: gui.new_game() # idem come sopra
        else:
            if eaten : food.respawn(snake, grid)
            if not TEST_MODE:
                gui.window.fill(colors.BLACK)
                grid.draw_path(pygame, gui.window, player.get_path_to_draw())
                snake.draw(pygame, gui.window, grid)
                grid.draw_obstacles(pygame, gui.window)
                food.draw(pygame, gui.window, grid)
                pygame.display.update()

### game start ###
if not TEST_MODE: # normal execution
    gui.snake_interface()
    config = 'default.config'
    log_file = 'default_log_file.config'
    if gui.dict_info['type']=='greedy':
        config = greedy_configs_fold+'bot3.config'
        log_file = greedy_configs_fold+'log1.json'
    if gui.dict_info['type']=='hamilton':
        config = hamilton_configs_fold+'bot6.config'
        log_file = hamilton_configs_fold+'log6.json'
    start_params = {
        'size': gui.SIZE,
        'x_blocks': gui.X_BLOCKS,
        'y_blocks': gui.Y_BLOCKS,
        'frame_delay': gui.FRAME_DELAY,
        'obstacles': gui.OBSTACLES,
        'autostart': gui.AUTOSTART,
        'executions': np.inf,
        'player_info': gui.dict_info,
        'bot_config': config,
        'log_file': log_file
    }
    start(start_params)
else: # execute to collect data for tests
    player_info = {
        'color': colors.GREEN,
        'start_location': 'top-left'
    }
    # get configurations parameters from file and start executions
    print('------ Bot greedy ------')
    for config_file, log_file in zip(greedy_configs, greedy_logs):
        print('config = %s'%config_file)
        player_info['type'] = 'greedy'
        start_params = get_game_config(greedy_configs_fold+'game.config')
        start_params['player_info'] = player_info
        start_params['bot_config'] = config_file
        start_params['log_file'] = log_file
        start(start_params)

    print('------ Bot hamilton ------')
    for config_file, log_file in zip(hamilton_configs, ham_logs):
        print('config = %s'%config_file)
        player_info['type'] = 'hamilton'
        start_params = get_game_config(hamilton_configs_fold+'game.config')
        start_params['player_info'] = player_info
        start_params['bot_config'] = config_file
        start_params['log_file'] = log_file
        start(start_params)