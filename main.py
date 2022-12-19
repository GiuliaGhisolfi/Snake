import pygame
import numpy as np
import time
from grid import Grid
from human_player import HumanPlayer
from bot_greedy import Bot_greedy
from bot_hamilton import Bot_hamilton
from bot_blind import *
from bot_random import *
from snake import Snake
from food import Food
import gui
import colors

TEST_MODE = True

def start(size, x_blocks, y_blocks, frame_delay, obstacle, autostart, max_repetitions, dict_info, bot_config, iterations_log):
    #create the window for the game
    pygame.init()
    grid = Grid(size, x_blocks, y_blocks)
    gui.window = pygame.display.set_mode(grid.bounds)
    pygame.display.set_caption("Snake")

    if obstacle == "None":
        grid.update_grid_dimensions(x_blocks, y_blocks)

    players_info = dict_info # retrieve the dictonary for the selected bot

    # create SNAKE, OBSTACLES if selected and FOOD
    snake = Snake(
            color = players_info["color"],
            start_location = players_info["start_location"])
    snake.respawn(grid)
    
    if obstacle != "None": 
        grid.spawn_obstacles(obstacle)
    
    food = Food(colors.RED)
    food.respawn(snake, grid)

    # bot selection
    if players_info["type"] == "human":
        player = HumanPlayer(
            game=pygame,
            up_key=players_info["keys"]["up"],
            down_key=players_info["keys"]["down"],
            right_key=players_info["keys"]["right"],
            left_key=players_info["keys"]["left"])
    elif players_info['type'] == "greedy":
        player = Bot_greedy(grid, snake, food, bot_config, iterations_log)
    elif players_info['type'] == 'hamilton':
        player = Bot_hamilton(grid, snake, food, bot_config, iterations_log, obstacle)
    elif players_info['type'] == 'blind':
        player = Bot_blind(grid, snake, food)
    elif players_info['type'] == 'random':
        player = Bot_random(grid, snake, food)
    else:
        print('PLAYERS INFO ERROR: player type not recognized')
        exit(1)

    repetitions = 0

    while repetitions < max_repetitions:
        pygame.time.delay(frame_delay)
        # exit the game if I click the x button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # retrieve next move
        dir = player.get_next_move()
        
        # check if eaten
        eaten = snake.move(dir, food)
        
        # check if lose
        lost = snake.bounds_collision(grid) or \
            snake.tail_collision()
        if lost:
            text = gui.font.render('GAME OVER', True, colors.RED)
            gui.window.blit(text, (gui.window.get_size()[0]/3, gui.window.get_size()[1]/3))  
            pygame.display.update()
            pygame.time.delay(gui.DEATH_DELAY)
            
            player.save_data()
            repetitions += 1
            snake.respawn(grid)
            if obstacle != "None" : grid.spawn_obstacles(obstacle)
            food.respawn(snake, grid)
            if not autostart: gui.new_game()

        # check if win
        if snake.length == grid.get_grid_free_area():
            snake.draw(pygame, gui.window, grid)
            grid.draw_obstacles(pygame, gui.window)
            snake.draw(pygame, gui.window, grid)
            text = gui.font.render('COMPLETE', True, colors.RED)
            gui.window.blit(text, (gui.window.get_size()[0]/3, gui.window.get_size()[1]/2))
            pygame.display.update()
            pygame.time.delay(gui.DEATH_DELAY)
            
            player.save_data()
            repetitions += 1
            snake.respawn(grid)
            if obstacle != "None": grid.spawn_obstacles(obstacle)
            food.respawn(snake, grid)
            if not autostart: gui.new_game()
        else:
            if eaten : food.respawn(snake, grid)
            gui.window.fill(colors.BLACK)

            grid.draw_path(pygame, gui.window, player.get_path_to_draw()) # display the path wich the snake is following
            snake.draw(pygame, gui.window, grid)
            grid.draw_obstacles(pygame, gui.window)
            food.draw(pygame, gui.window, grid)
            pygame.display.update()


def parse_config(file):
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

        try:
            size = int(param['size'])
            x_blocks = int(param['x_blocks'])
            y_blocks = int(param['y_blocks'])
            frame_delay = int(param['frame_delay'])
            obstacle = str(param['obstacle']) 
            autostart = bool(param['autostart'])
            repetitions = int(param['repetitions'])

        except Exception as e:
            print(e)
            print('parameter value error')
            print('initialization with default values')

            size = 700
            x_blocks = 10
            y_blocks = 11
            frame_delay = 1
            obstacle = 'None'
            autostart = True
            repetitions = 30
        
        return size, x_blocks, y_blocks, frame_delay, obstacle, autostart, repetitions


greedy_fold = './dati_greedy/'
greedy_configs = [
    greedy_fold+'c1.config', 
    greedy_fold+'c2.config', 
    greedy_fold+'c3.config',
    greedy_fold+'c4.config',
    greedy_fold+'c5.config',
    greedy_fold+'c6.config',
    greedy_fold+'c7.config'
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
ham_fold = './dati_hamilton/'
ham_configs = [
    ham_fold+'c1.config', 
    ham_fold+'c2.config', 
    ham_fold+'c3.config',
    ham_fold+'c4.config',
    ham_fold+'c5.config',
    ham_fold+'c6.config',
    ham_fold+'c7.config',
    ham_fold+'c8.config',
    ham_fold+'c9.config',
    ham_fold+'c10.config',
    ham_fold+'c11.config'
    ]
ham_logs = [
    ham_fold+'log1.json', 
    ham_fold+'log2.json', 
    ham_fold+'log3.json',
    ham_fold+'log4.json',
    ham_fold+'log5.json',
    ham_fold+'log6.json',
    ham_fold+'log7.json',
    ham_fold+'log8.json',
    ham_fold+'log9.json',
    ham_fold+'log10.json',
    ham_fold+'log11.json'
    ]


### game start ###
if not TEST_MODE:
    gui.snake_interface()

    if gui.dict_info_single['type']=='greedy':
        config = './dati_greedy/c7.config'
        iterations_log = './dati_greedy/log7.json'
    if gui.dict_info_single['type']=='hamilton':
        config = './dati_hamilton/c11.config'
        iterations_log = './dati_hamilton/log11.json'

    start(size=gui.SIZE, 
    x_blocks=gui.X_BLOCKS, 
    y_blocks=gui.Y_BLOCKS, 
    frame_delay=gui.FRAME_DELAY, 
    obstacle=gui.OBSTACLES, 
    autostart=gui.AUTOSTART,
    max_repetitions=np.inf,
    dict_info=gui.dict_info_single,
    bot_config=config,
    iterations_log=iterations_log
    )
else:
    for conf, log in zip(greedy_configs, greedy_logs):
        dictionary = { 
            "type": "greedy",
            "color": colors.GREEN,
            "start_location": "top-left"
        }
        size, x_blocks, y_blocks, frame_delay, obstacle, autostart, repetitions = parse_config('./dati_greedy/main.config')
        start(size, x_blocks, y_blocks, frame_delay, obstacle, autostart, repetitions, dictionary, conf, log)


    for conf, log in zip(ham_configs, ham_logs):
        dictionary = { 
            "type": "hamilton",
            "color": colors.GREEN,
            "start_location": "top-left"
        }
        size, x_blocks, y_blocks, frame_delay, obstacle, autostart, repetitions = parse_config('./dati_hamilton/main.config')
        start(size, x_blocks, y_blocks, frame_delay, obstacle, autostart, repetitions, dictionary, conf, log)