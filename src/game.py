import pygame
import random as r
from enum import Enum
from src.grid import Grid
from src.human_player import HumanPlayer
from src.bot_greedy import BotGreedy
from src.bot_hamilton import BotHamilton
from src.bot_blind import BotBlind
from src.bot_random import BotRandom
from src.snake import Snake
from src.food import Food
from src.config_parsing import *
import src.gui as gui
import src.colors as colors

DEATH_DELAY = 700

def run_game(
    grid_size,
    grid_width,
    grid_height,
    frame_delay,
    obstacles,
    autostart,
    max_executions,
    player_info,
    bot_config,
    log_file,
    test_mode
    ):

    # create the game grid
    grid = Grid(grid_size, grid_width, grid_height)

    # create the window for the game
    if not test_mode:
        pygame.init()
        gui.window = pygame.display.set_mode(grid.bounds)
        pygame.display.set_caption('Snake')
        grid.update_grid_dimensions(grid_width, grid_height)

    # create snake, obstacles and food
    snake = Snake(color=colors.GREEN)
    snake.respawn()
    grid.spawn_obstacles(obstacles)
    food = Food(colors.RED)
    food.respawn(snake, grid)

    # selects the player
    if player_info == 'human':
        player = HumanPlayer(pygame, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)
    elif player_info == 'greedy':
        player = BotGreedy(grid, snake, food, bot_config, log_file, test_mode)
    elif player_info == 'hamilton':
        player = BotHamilton(grid, snake, food, bot_config, log_file, obstacles, test_mode)
    elif player_info == 'blind':
        player = BotBlind(grid, snake, food, test_mode)
    else:
        player = BotRandom(grid, snake, food, test_mode)

    executions = 0
    while (executions < max_executions):
        if not test_mode:
            pygame.time.delay(frame_delay)
            # exit the game if the 'x' button has been clicked
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    executions = max_executions

        # retrieve player's next move
        dir = player.get_next_move()
        
        # move the snake
        has_eaten = snake.move(dir, food)
        
        # check if crashed
        crashed = snake.bounds_collision(grid) or snake.tail_collision()

        if not crashed and snake.length != grid.get_grid_free_area(): # game continues
            if has_eaten : 
                food.respawn(snake, grid)
            if not test_mode:
                gui.window.fill(colors.BLACK)
                grid.draw_path(pygame, gui.window, player.get_path_to_draw())
                snake.draw(pygame, gui.window, grid)
                grid.draw_obstacles(pygame, gui.window)
                food.draw(pygame, gui.window, grid)
                pygame.display.update()
        else: # game ended
            if test_mode:
                executions += 1
                player.write_log(executions==max_executions, crashed)
                print('Execution %d/%d'%(executions, max_executions))
            if crashed: # has lost
                text = gui.font1.render('GAME OVER', True, colors.PURPLE)
                gui.window.blit(text, ((gui.window.get_size()[0]-text.get_width())/2,(gui.window.get_size()[1]-text.get_height())/2))
                pygame.display.update()
                pygame.time.delay(DEATH_DELAY)
            else: # has won
                snake.draw(pygame, gui.window, grid)
                grid.draw_obstacles(pygame, gui.window)
                snake.draw(pygame, gui.window, grid)
                text = gui.font1.render('WIN', True, colors.PURPLE)
                gui.window.blit(text, ((gui.window.get_size()[0]-text.get_width())/2, (gui.window.get_size()[1]-text.get_height())/2))
                pygame.display.update()
                pygame.time.delay(DEATH_DELAY)
            player.set_restart_game()
            snake.respawn()
            grid.spawn_obstacles(obstacles)
            food.respawn(snake, grid)
            if not autostart: 
                gui.new_game()