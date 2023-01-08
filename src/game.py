import pygame, sys
from src.grid import Grid
from src.human_player import HumanPlayer
from src.bot_greedy import Bot_greedy
from src.bot_hamilton import Bot_hamilton
from src.bot_blind import Bot_blind
from src.bot_random import Bot_random
from src.snake import Snake
from src.food import Food
from src.config_parsing import *
import src.gui as gui
import src.colors as colors

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
    log_file,
    test_mode
    ):
    #def start(params):
    # parameters initialization
    """size = params['size']
    x_blocks = params['x_blocks']
    y_blocks = params['y_blocks']
    frame_delay = params['frame_delay']
    obstacles = params['obstacles']
    autostart = params['autostart']
    max_executions = params['executions']
    player_info = params['player_info']
    bot_config = params['bot_config']
    log_file = params['log_file']
    test_mode = params['test_mode']"""

    grid = Grid(size, x_blocks, y_blocks)

    # create the window for the game
    if not test_mode:
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
        player = Bot_greedy(grid, snake, food, bot_config, log_file, test_mode)
    elif player_info['type'] == 'hamilton':
        player = Bot_hamilton(grid, snake, food, bot_config, log_file, obstacles, test_mode)
    elif player_info['type'] == 'blind':
        player = Bot_blind(grid, snake, food, test_mode)
    elif player_info['type'] == 'random':
        player = Bot_random(grid, snake, food, test_mode)
    else:
        print('PLAYERS INFO ERROR: player type not recognized')
        exit(1)

    executions = 0
    while (executions < max_executions) and (executions < sys.maxsize): # così non va in overflow, ed è plausibile che l'utente non voglia fare più 9*(10^18) esecuzioni di fila
        if not test_mode:
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
            if test_mode:
                print('Execution %d/%d'%(executions+1, max_executions))
            else:
                text = gui.font.render('GAME OVER', True, colors.RED)
                gui.window.blit(text, (gui.window.get_size()[0]/3, gui.window.get_size()[1]/3))  
                pygame.display.update()
                pygame.time.delay(gui.DEATH_DELAY)
            
            executions += 1
            if test_mode:
                player.write_log(executions==max_executions, lost)
            snake.respawn(grid)
            grid.spawn_obstacles(obstacles)
            food.respawn(snake, grid)
            if not autostart: gui.new_game() # con test mode è sempre autostart, lasciamo comunque così?
            player.set_restart_game()
        elif snake.length == grid.get_grid_free_area(): # win
            if test_mode:
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
            if test_mode:
                player.write_log(executions==max_executions, lost)
            snake.respawn(grid)
            grid.spawn_obstacles(obstacles)
            food.respawn(snake, grid)
            if not autostart: gui.new_game() # idem come sopra
            player.set_restart_game()
        else:
            if eaten : food.respawn(snake, grid)
            if not test_mode:
                gui.window.fill(colors.BLACK)
                grid.draw_path(pygame, gui.window, player.get_path_to_draw())
                snake.draw(pygame, gui.window, grid)
                grid.draw_obstacles(pygame, gui.window)
                food.draw(pygame, gui.window, grid)
                pygame.display.update()