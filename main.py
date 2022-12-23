import pygame
import numpy as np
from grid import Grid
from human_player import HumanPlayer
from bot_greedy import Bot_greedy
from bot_hamilton import Bot_hamilton
from bot_blind import *
from bot_random import *
from snake import Snake
from food import Food
from config_parsing import get_game_config
import gui
import colors

TEST_MODE = False

def start(
    size, 
    x_blocks, 
    y_blocks, 
    frame_delay, 
    obstacles, 
    autostart, 
    max_executions, 
    player_info,
    bot_config, 
    log_file
    ):

    grid = Grid(size, x_blocks, y_blocks)

    # create the window for the game
    if not TEST_MODE:
        pygame.init()
        gui.window = pygame.display.set_mode(grid.bounds)
        pygame.display.set_caption('Snake')
        grid.update_grid_dimensions(x_blocks, y_blocks) # REVIEW: quando TEST_MODE==True serve?

    # create snake, obstacles and food
    snake = Snake(color = player_info['color'], start_location = player_info['start_location'])
    snake.respawn(grid)
    grid.spawn_obstacles(obstacles)
    food = Food(colors.RED)
    food.respawn(snake, grid)

    # bot selection
    if not TEST_MODE and player_info['type'] == 'human': # REVIEW: in test mode non è mai human
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
    while executions < max_executions: # TODO: sistemare overflow con np.inf?
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
                player.save_data(executions==max_executions)
            snake.respawn(grid)
            grid.spawn_obstacles(obstacles)
            food.respawn(snake, grid)
            if not autostart: gui.new_game() # REVIEW: con test mode è sempre autostart
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
            player.save_data(executions==max_executions)
            snake.respawn(grid)
            grid.spawn_obstacles(obstacles)
            food.respawn(snake, grid)
            if not autostart: gui.new_game() # REVIEW: con test mode è sempre autostart
        else:
            if eaten : food.respawn(snake, grid)
            if not TEST_MODE:
                gui.window.fill(colors.BLACK)
                grid.draw_path(pygame, gui.window, player.get_path_to_draw())
                snake.draw(pygame, gui.window, grid)
                grid.draw_obstacles(pygame, gui.window)
                food.draw(pygame, gui.window, grid)
                pygame.display.update()
###
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
###
### game start ###
if not TEST_MODE:
    gui.snake_interface()
    config = 'default.config'
    log_file = 'default_log_file.config'
    if gui.dict_info['type']=='greedy':
        config = greedy_fold+'bot7.config'
        log_file = greedy_fold+'log7.json'
    if gui.dict_info['type']=='hamilton':
        config = hamilton_fold+'bot6.config'
        log_file = hamilton_fold+'log6.json'
    start(
        size=gui.SIZE, 
        x_blocks=gui.X_BLOCKS, 
        y_blocks=gui.Y_BLOCKS, 
        frame_delay=gui.FRAME_DELAY, 
        obstacles=gui.OBSTACLES, 
        autostart=gui.AUTOSTART,
        max_executions=np.inf,
        player_info=gui.dict_info,
        bot_config=config,
        log_file=log_file
    )
else:
    player_info = {
        'color': colors.GREEN,
        'start_location': 'top-left'
    }
    print('------ Bot greedy ------')
    for config_file, log_file in zip(greedy_configs, greedy_logs):
        print('config = %s'%config_file)
        player_info['type'] = 'greedy'
        size, x_blocks, y_blocks, frame_delay, obstacles, autostart, executions = get_game_config(greedy_fold+'game.config')
        start(
            size=size, 
            x_blocks=x_blocks, 
            y_blocks=y_blocks, 
            frame_delay=frame_delay, 
            obstacles=obstacles, 
            autostart=autostart, 
            max_executions=executions, 
            player_info=player_info, 
            bot_config=config_file,
            log_file=log_file
        )

    print('------ Bot hamilton ------')
    for config_file, log_file in zip(hamilton_configs, ham_logs):
        print('config = %s'%config_file)
        player_info['type'] = 'hamilton'
        size, x_blocks, y_blocks, frame_delay, obstacles, autostart, executions = get_game_config(hamilton_fold+'game.config')
        start(
            size=size, 
            x_blocks=x_blocks, 
            y_blocks=y_blocks, 
            frame_delay=frame_delay, 
            obstacles=obstacles, 
            autostart=autostart, 
            max_executions=executions, 
            player_info=player_info, 
            bot_config=config_file, 
            log_file=log_file
        )

"""
TODO:
-   organizzare meglio il main, magari spostare le costanti (i path dei file di configurazione) in un altro file? controllare i REVIEW:
-   sistemare get_game_config (evitare di fargli ritornare tutti quei parametri, raggrupparli)
-   capire se i dati che salviamo sono tutti quelli che possono servirci e provare a processarli per capire se è comodo il formato che usiamo per scriverli
-   aggiungere test per i bot random
-   sistemare file gui (ci sono troppe costanti a cui accediamo supponendo che venga invocato il metodo snake_interface)
-   bisognerebbe fondere search e utils, togliere le cose che non servono e forse mettere nello stesso file le nostre versioni di a*
-   aggiungere commenti al nuovo codice e ripulirlo
-   uniformare il passaggio di parametri a funzioni (esplicitiamo il tipo in tutte?)
-   importare cose specifiche, evitare *
"""