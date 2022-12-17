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


def start():
    pygame.init()
    grid = Grid(size=gui.SIZE, x_blocks=gui.X_BLOCKS, y_blocks=gui.Y_BLOCKS)
    gui.window = pygame.display.set_mode(grid.bounds)
    pygame.display.set_caption("Snake")

    info_string = '[' + str(gui.X_BLOCKS) + '|' + str(gui.Y_BLOCKS) + '|' + str(gui.OBSTACLES) + '|' + str(gui.FRAME_DELAY) + ']'

    if gui.OBSTACLES == "None":
        grid.update_grid_dimensions(gui.X_BLOCKS, gui.Y_BLOCKS)

    players_info = gui.dict_info_single # retrieve the dictonary for the selected bot
    # create snake, food and obstacles if selected
    """players_info = { 
    "type": 'random',
    "color": colors.ORANGE,
    "start_location": "top-left",
    "keys": {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "right": pygame.K_RIGHT,
        "left": pygame.K_LEFT
    } 
} """

    snake = Snake(
            color=players_info["color"],
            start_location=players_info["start_location"])
    snake.respawn(grid)
    
    if gui.OBSTACLES != "None": 
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
        player = Bot_greedy(grid, snake, food, info=info_string)
    elif players_info['type'] == 'hamilton':
        player = Bot_hamilton(grid, snake, food)
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
        pygame.time.delay(gui.FRAME_DELAY)
        # exit the game if i click the x button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                #file.close()

        # retrieve next move
        dir = player.get_next_move()
        # check if eaten
        eaten = snake.move(dir, food)
        # check if lose
        # lost = False
        lost = snake.bounds_collision(grid) or \
            snake.tail_collision()

        if lost:
            text = gui.font.render('GAME OVER', True, colors.RED)
            gui.window.blit(text, (gui.window.get_size()[0]/3, gui.window.get_size()[1]/3))  
            pygame.display.update()
            pygame.time.delay(gui.DEATH_DELAY)
            
            player.save_data(0)
            snake.respawn(grid)
            if gui.OBSTACLES != "None": grid.spawn_obstacles()
            food.respawn(snake, grid)
            steps = 0
            if not gui.AUTOSTART: gui.new_game()
        # check if win
        if snake.length == grid.get_grid_free_area():
            snake.draw(pygame, gui.window, grid)
            grid.draw_obstacles(pygame, gui.window)
            snake.draw(pygame, gui.window, grid)
            text = gui.font.render('COMPLETE', True, colors.RED)
            gui.window.blit(text, (gui.window.get_size()[0]/3, gui.window.get_size()[1]/2))
            pygame.display.update()
            pygame.time.delay(gui.DEATH_DELAY)
            
            player.save_data(1)
            snake.respawn(grid)
            if gui.OBSTACLES != "None":
                grid.spawn_obstacles()
            food.respawn(snake, grid)
            if not gui.AUTOSTART: gui.new_game()
        else:
            if eaten:
                food.respawn(snake, grid)
            gui.window.fill(colors.BLACK)

            grid.draw_path(pygame, gui.window, player.get_path_to_draw())
            snake.draw(pygame, gui.window, grid)
            grid.draw_obstacles(pygame, gui.window)
            food.draw(pygame, gui.window, grid)
            pygame.display.update()


### game start ###
gui.snake_interface()
start()