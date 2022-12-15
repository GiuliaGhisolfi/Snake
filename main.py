import pygame
from grid import Grid
from human_player import HumanPlayer
from bot_singleplayer import Bot_singleplayer
from bot_hamilton import Bot_hamilton
from snake import Snake
from food import Food
import button
import colors
import directions
import time

pygame.init()
grid = Grid(size=button.SIZE, x_blocks=button.X_BLOCKS, y_blocks=button.Y_BLOCKS)
button.window = pygame.display.set_mode(grid.bounds)
pygame.display.set_caption("Snake")

def human_start():
    players_info = button.dict_info_single # retrieve the dictonary for the selected bot
    snakes = [] # list of snake
    # create snake, food and obstacles if selected
    snake = Snake(
            color=players_info["color"],
            start_location=players_info["start_location"])
    snake.respawn(grid)
    snakes.append(snake)
    if button.OBSTACLES != "None": 
        grid.spawn_obstacles()
    food = Food(colors.RED)
    food.respawn(snakes, grid)
    # logs
    file = open("player0"+"_logfile.csv", "w")
    file.write("OUTCOME,LENGTH,STEPS\n")
    # bot selection
    if players_info["type"] == "human":
        player = HumanPlayer(
            game=pygame,
            up_key=players_info["keys"]["up"],
            down_key=players_info["keys"]["down"],
            right_key=players_info["keys"]["right"],
            left_key=players_info["keys"]["left"])
    else:
        print('PLAYERS INFO ERROR: player type not recognized')
        exit(1)
    # variables used in the while loop
    steps = 0
    run = True

    GAMEOVER_FILE = open('gameOverLog.cvs', 'w+')
    GAMEOVER_FILE.write('CORPO,CIBO\n')
    # while until I exit the game
    while run:
        if len(snake.get_body()) != snake.length: print('ops')
        steps = steps + 1
        pygame.time.delay(button.FRAME_DELAY)
        # exit the game if i click the x button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                file.close()
                GAMEOVER_FILE.close()
        # retrieve next move
        dir = player.get_next_move()
        # check if eaten
        eaten = snake.move(dir, food)
        # check if lose
        lost = False
        lost = snake.bounds_collision(grid) or \
            snake.tail_collision()
        if lost:
            text = button.font.render('GAME OVER', True, colors.RED)
            button.window.blit(text, (button.window.get_size()[0]/3, button.window.get_size()[1]/3))  
            pygame.display.update()
            pygame.time.delay(700)
            file.write("%s,%s\n" % (snake.length, steps))

            GAMEOVER_FILE.write(str(snake.get_body()))
            GAMEOVER_FILE.write(',')
            GAMEOVER_FILE.write(str(food.position))
            GAMEOVER_FILE.write('\n')
            
            snake.respawn(grid)
            if button.OBSTACLES != "None": grid.spawn_obstacles()
            food.respawn(snakes, grid)
            steps = 0
            button.new_game()
        # check if win
        if snake.length == grid.get_grid_free_area():
            grid.draw_path(pygame, button.window, [player.path_to_food, player.default_path], [colors.YELLOW, colors.WHITE], [False, True])
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            snake.draw(pygame, button.window, grid)
            text = button.font.render('COMPLETE', True, colors.RED)
            button.window.blit(text, (button.window.get_size()[0]/3, button.window.get_size()[1]/2))
            pygame.display.update()
            pygame.time.delay(700)
            snake.respawn(grid)
            if button.OBSTACLES != "None":
                grid.spawn_obstacles()
            food.respawn(snakes, grid)
            button.new_game()
        else:
            if eaten:
                food.respawn(snakes, grid)
            button.window.fill(colors.BLACK)
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            food.draw(pygame, button.window, grid)
            pygame.display.update()

def greedy_start():
    players_info = button.dict_info_single # retrieve the dictonary for the selected bot
    snakes = [] # list of snake
    # create snake, food and obstacles if selected
    snake = Snake(
            color=players_info["color"],
            start_location=players_info["start_location"])
    snake.respawn(grid)
    snakes.append(snake)
    if button.OBSTACLES != "None": 
        grid.spawn_obstacles()
    food = Food(colors.RED)
    food.respawn(snakes, grid)
    # log
    file = open("player0"+"_logfile.csv", "w")
    file.write("OUTCOME,LENGTH,STEPS\n")
    # bot selection
    if players_info["type"] == "greedy":
        player = Bot_singleplayer(grid, snakes[0], food, True)
    else:
        print('PLAYERS INFO ERROR: player type not recognized')
        exit(1)
    # variables used in the while loop
    steps = 0
    run = True

    GAMEOVER_FILE = open('gameOverLog.cvs', 'w+')
    GAMEOVER_FILE.write('CORPO,CIBO\n')
    # loop until I exit the game
    while run:
        if len(snake.get_body()) != snake.length: print('ops')
        steps = steps + 1
        pygame.time.delay(button.FRAME_DELAY)
        # exit the game if I click the x button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                file.close()
                GAMEOVER_FILE.close()
        # compute next move
        dir = player.get_next_move()
        # check if bot stucks in a loop
        if dir != directions.Directions.CLOSE:
            eaten = snake.move(dir, food)
            lost = False
            lost = snake.bounds_collision(grid) or \
                snake.tail_collision()
            if lost:
                text = button.font.render('GAME OVER', True, colors.RED)
                button.window.blit(text, (button.window.get_size()[0]/3, button.window.get_size()[1]/3))
                pygame.display.update()
                pygame.time.delay(700)
                file.write("%s,%s\n" % (snake.length, steps))

                GAMEOVER_FILE.write(str(snake.get_body()))
                GAMEOVER_FILE.write(',')
                GAMEOVER_FILE.write(str(food.position))
                GAMEOVER_FILE.write('\n')
                
                snake.respawn(grid)
                if button.OBSTACLES != "None":
                    grid.spawn_obstacles()
                food.respawn(snakes, grid)
                steps = 0
                button.new_game()
        else:
            text = button.font.render('LOOP', True, colors.RED)
            button.window.blit(text, (button.window.get_size()[0]/3, button.window.get_size()[1]/3))
            pygame.display.update()
            pygame.time.delay(700)
            file.write("%s,%s\n" % (snake.length, steps))

            GAMEOVER_FILE.write(str(snake.get_body()))
            GAMEOVER_FILE.write(',')
            GAMEOVER_FILE.write(str(food.position))
            GAMEOVER_FILE.write('\n')
            
            snake.respawn(grid)
            if button.OBSTACLES != "None":
                grid.spawn_obstacles()
            food.respawn(snakes, grid)
            steps = 0
            button.new_game()     
        # check if I win
        if snake.length == grid.get_grid_free_area():
            grid.draw_path(pygame, button.window, [player.path_to_food, player.default_path], [colors.YELLOW, colors.WHITE], [False, True])
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            snake.draw(pygame, button.window, grid)
            text = button.font.render('COMPLETE', True, colors.RED)
            button.window.blit(text, (button.window.get_size()[0]/3, button.window.get_size()[1]/3))
            pygame.display.update()
            pygame.time.delay(700)
            snake.respawn(grid)
            if button.OBSTACLES != "None": 
                grid.spawn_obstacles()
            food.respawn(snakes, grid)
            button.new_game()
        else:
            if eaten:
                food.respawn(snakes, grid)
            button.window.fill(colors.BLACK)
            grid.draw_path(pygame, button.window, [player.default_path, player.path_to_food], [colors.YELLOW, colors.RED], [True, False])
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            food.draw(pygame, button.window, grid)
            pygame.display.update()


def hamilton_start():
    players_info = button.dict_info_single # retrieve the dictonary for the selected bot
    snakes = [] # list of snake
    steps_time = [] # creates a list with the time for each iteration 
    # create snake, food and obstacles if selected
    snake = Snake(
            color=players_info["color"],
            start_location=players_info["start_location"])
    snake.respawn(grid)
    snakes.append(snake)
    if button.OBSTACLES != "None":
        grid.spawn_obstacles()
    food = Food(colors.RED)
    food.respawn(snakes, grid)
    # logs
    file = open("player0"+"_logfile.csv", "w")
    file.write("OUTCOME,LENGTH,STEPS\n")
    # bot selection
    if players_info["type"] == "hamilton":
        player = Bot_hamilton(grid, snakes[0], food)
    else:
        print('PLAYERS INFO ERROR: player type not recognized')
        exit(1)
    # variables used in the while loop
    steps = 0
    run = True

    GAMEOVER_FILE = open('gameOverLog.cvs', 'w+')
    GAMEOVER_FILE.write('COMPLETE, CONFIGURATION, TIME, STEPS\n')
    ITERATION_TIME = open('IterationTime.cvs', 'w+')
    ITERATION_TIME.write('STEPS, TIME\n')
    
    eaten = False
    tic = time.time()
    # while until I exit the game
    while run:
        steps = steps + 1
        iter_tic = time.time()
        pygame.time.delay(button.FRAME_DELAY)
        # exit the game if i click the x button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                file.close()
                GAMEOVER_FILE.close()
        # compute next move
        dir = player.get_next_move(alpha=0.5, beta=0.5)
        # alpha: snake.length/grid_area s.t. stops greedy algh        
        # beta: snake.length/grid_area s.t. stops dynamic algh
        # check if snake eat
        eaten = snake.move(dir, food)
        # check if lose
        lost = snake.bounds_collision(grid) or \
            snake.tail_collision()
        #retrieve hamilton cycle
        ham_cycle = {}
        if steps == 1:
            ham_cycle = player.return_cycle(first_step=True)
            ham_cycle_changed = True
        else:
            ham_cycle = player.return_cycle(first_step=False) 
        end = False
        if lost:
            end = True
            text = button.font.render('GAME OVER', True, colors.RED)
            button.window.blit(text, (button.window.get_size()[0]/3, button.window.get_size()[1]/3))
        if end:
            pygame.display.update()
            pygame.time.delay(700)
            # write info in docs
            file.write("%s,%s\n" % (snake.length, steps))
            iter_toc = time.time()
            steps_time.append(iter_toc - iter_tic)
            ITERATION_TIME.write(str(steps))
            ITERATION_TIME.write(', ')
            ITERATION_TIME.write(str(iter_toc - iter_tic))
            ITERATION_TIME.write('\n')
            GAMEOVER_FILE.write(str(snake.body))
            GAMEOVER_FILE.write(',')
            GAMEOVER_FILE.write(str(food.position))
            GAMEOVER_FILE.write('\n')
            
            snake.respawn(grid)
            if button.OBSTACLES != "None":
                grid.spawn_obstacles()
            player.update_ham_cycle()
            food.respawn(snakes, grid)
            button.new_game()
        # check if win
        if snake.length == grid.get_grid_free_area():
            toc = time.time()
            grid.draw_cycle(pygame, button.window, ham_cycle, ham_cycle_changed)
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            text = button.font.render('COMPLETE', True, colors.RED)
            button.window.blit(text, (button.window.get_size()[0]/3, button.window.get_size()[1]/2))
            pygame.display.update()
            iter_toc = time.time()
            steps_time.append(iter_toc - iter_tic)
            steps_time = []

            ITERATION_TIME.write(str(steps))
            ITERATION_TIME.write(', ')
            ITERATION_TIME.write(str(iter_toc - iter_tic))
            ITERATION_TIME.write('\n') 
            GAMEOVER_FILE.write('Complete')
            GAMEOVER_FILE.write(', ')
            GAMEOVER_FILE.write(str(grid.current_config))
            GAMEOVER_FILE.write(', ')
            GAMEOVER_FILE.write(str(toc - tic))
            GAMEOVER_FILE.write(', ')
            GAMEOVER_FILE.write(str(steps))
            GAMEOVER_FILE.write('\n')
            
            pygame.time.delay(700)            
            steps = 0
            tic = time.time()
            snake.respawn(grid)
            if button.OBSTACLES != "None":
                grid.spawn_obstacles()
                player.update_ham_cycle()                
            food.respawn(snakes, grid)
            button.new_game()
        # just continue for the next iteration
        else:
            if eaten:
                food.respawn(snakes, grid)
            button.window.fill(colors.BLACK)
            grid.draw_cycle(pygame, button.window, ham_cycle, ham_cycle_changed)
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            food.draw(pygame, button.window, grid)
            pygame.display.update()

def select_start():
    if button.OBSTACLES == "None":
        grid.update_grid_dimensions(button.X_BLOCKS, button.Y_BLOCKS)
    if button.choise_made == 'hamilton':
        hamilton_start()
    elif button.choise_made == 'human':
        human_start()
    elif button.choise_made == 'astar':
        greedy_start()
    else:
        print("choise not recognized")
        exit()

### game start ###
button.snake_interface()
select_start()