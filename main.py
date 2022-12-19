import pygame
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
config = '.\dati_hamilton\c11.config'
iterations_log = '.\dati_hamilton\log11.json'

def start(size, x_blocks, y_blocks, frame_delay, obstacle, autostart):
    #create the window for the game
    pygame.init()
    grid = Grid(size, x_blocks, y_blocks)
    gui.window = pygame.display.set_mode(grid.bounds)
    pygame.display.set_caption("Snake")

    if obstacle == "None":
        grid.update_grid_dimensions(x_blocks, y_blocks)

    players_info = gui.dict_info_single # retrieve the dictonary for the selected bot

    # create SNAKE, OBSTACLES if selected and FOOD
    snake = Snake(
            color = players_info["color"],
            start_location = players_info["start_location"])
    snake.respawn(grid)
    
    if obstacle != "None": 
        grid.spawn_obstacles()   
    
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
        player = Bot_greedy(grid, snake, food, config, iterations_log)
    elif players_info['type'] == 'hamilton':
        player = Bot_hamilton(grid, snake, food, config, iterations_log)
    elif players_info['type'] == 'blind':
        player = Bot_blind(grid, snake, food)
    elif players_info['type'] == 'random':
        player = Bot_random(grid, snake, food)
    else:
        print('PLAYERS INFO ERROR: player type not recognized')
        exit(1)

    # variables used in the while loop
    steps = 0
    run = True

    while run:
        steps = steps + 1
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
            snake.respawn(grid)
            if obstacle != "None" : grid.spawn_obstacles()
            food.respawn(snake, grid)
            steps = 0
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
            snake.respawn(grid)
            if obstacle != "None": grid.spawn_obstacles()
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
        
        return size, x_blocks, y_blocks, frame_delay, obstacle, autostart

### game start ###
if not TEST_MODE:
    gui.snake_interface()    
    start(size=gui.SIZE, x_blocks=gui.X_BLOCKS, y_blocks=gui.Y_BLOCKS, frame_delay=gui.FRAME_DELAY, obstacle=gui.OBSTACLES, autostart=gui.AUTOSTART)
else:
    size, x_blocks, y_blocks, frame_delay, obstacle, autostart = parse_config('.\dati_hamilton\main.config')
    start(size, x_blocks, y_blocks, frame_delay, obstacle, autostart)