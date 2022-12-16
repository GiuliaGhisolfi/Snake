import pygame, sys
from concurrent.futures import ThreadPoolExecutor
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

FRAME_DELAY = 20
OBSTACLES = False
AUTOSTART = True

### if obstacle == True: X_BLOCKS = 15 and Y_BLOCKS = 16
X_BLOCKS = 6
Y_BLOCKS = 6
###
info_string = '[' + str(X_BLOCKS) + '|' + str(Y_BLOCKS) + '|' + str(OBSTACLES) + '|' + str(FRAME_DELAY) + ']'
pygame.init()
grid = Grid(size=700, x_blocks=X_BLOCKS, y_blocks=Y_BLOCKS, flag_obstacles=OBSTACLES)
window = pygame.display.set_mode(grid.bounds)
pygame.display.set_caption("Snake")
font = pygame.font.SysFont('Arial', 40, True)
clock = pygame.time.Clock()

def singleplayer_start():
    players_info = button.dict_info_single

    snakes = []

    # creo gli snake, poi il cibo e poi il o i bot, necessario per il bot sigleplayer
    snake = Snake(
            color=players_info["color"],
            start_location=players_info["start_location"])

    snake.respawn(grid)
    snakes.append(snake)
    if OBSTACLES: grid.spawn_obstacles()

    food = Food(colors.RED)
    food.respawn(snakes, grid)

    # logs
    file = open("player0"+"_logfile.csv", "w")
    file.write("OUTCOME,LENGTH,STEPS\n")

    # bots
    if players_info["type"] == "human":
        player = HumanPlayer(
            game=pygame,
            up_key=players_info["keys"]["up"],
            down_key=players_info["keys"]["down"],
            right_key=players_info["keys"]["right"],
            left_key=players_info["keys"]["left"])
    elif players_info["type"] == "sbot":
        player = Bot_singleplayer(grid, snakes[0], food, info=info_string)
    else:
        print('PLAYERS INFO ERROR: player type not recognized')
        exit(1)

    steps = 0
    run = True

    while run:
        if len(snake.get_body()) != snake.length: print('ops')
        steps = steps + 1

        pygame.time.delay(FRAME_DELAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                file.close()
   
        dir = player.get_next_move()
        mangiato = snake.move(dir, food)

        lost = snake.bounds_collision(grid) or \
            snake.tail_collision()

        end = False
        if lost:
            end = True
            text = button.font.render('GAME OVER', True, colors.FUXIA)
            button.window.blit(text, (180, 270))
            
        if end:
            pygame.display.update()
            pygame.time.delay(700)
            file.write("%s,%s\n" % (snake.length, steps))
            
            snake.respawn(grid)
            if OBSTACLES: grid.spawn_obstacles()
            food.respawn(snakes, grid)
            if players_info["type"] == 'sbot': player.save_data(False)

            steps = 0
            if not AUTOSTART: button.new_game()
        
        if snake.length == grid.get_grid_free_area():
            
            grid.draw_path(pygame, button.window, [player.path_to_food, player.default_path], [colors.YELLOW, colors.WHITE], [False, True])
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            snake.draw(pygame, button.window, grid)
            
            text = button.font.render('COMPLETE', True, colors.FUXIA)
            button.window.blit(text, (180, 270))
            
            pygame.display.update()
            pygame.time.delay(700)
            
            snake.respawn(grid)
            if OBSTACLES: grid.spawn_obstacles()
            food.respawn(snakes, grid)
            if players_info["type"] == 'sbot': player.save_data(True)
            if not AUTOSTART: button.new_game()
        else:
            if mangiato:
                food.respawn(snakes, grid)

            button.window.fill(colors.BLACK)
            if players_info["type"] == "sbot":
                grid.draw_path(pygame, button.window, [player.default_path, player.path_to_food], [colors.YELLOW, colors.RED], [True, False])
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            food.draw(pygame, button.window, grid)
            pygame.display.update()

def hamilton_start():
    players_info = button.dict_info_single

    snakes = []
    steps_time = [] # crea una lista con il tempo per ogni iterazione -> per ora non si usa

    # creo gli snake, poi il cibo e poi il o i bot, necessario per il bot sigleplayer
    snake = Snake(
            color=players_info["color"],
            start_location=players_info["start_location"])

    snake.respawn(grid)
    snakes.append(snake)
    if OBSTACLES: grid.spawn_obstacles()

    food = Food(colors.RED)
    food.respawn(snakes, grid)

    # logs
    file = open("player0"+"_logfile.csv", "w")
    file.write("OUTCOME,LENGTH,STEPS\n")

    # bots
    if players_info["type"] == "human":
        player = HumanPlayer(
            game=pygame,
            up_key=players_info["keys"]["up"],
            down_key=players_info["keys"]["down"],
            right_key=players_info["keys"]["right"],
            left_key=players_info["keys"]["left"])
    elif players_info["type"] == "sbot":
        player = Bot_hamilton(grid, snakes[0], food)
    else:
        print('PLAYERS INFO ERROR: player type not recognized')
        exit(1)

    steps = 0
    run = True

    # avvia il bot corretto
    GAMEOVER_FILE = open('gameOverLog.cvs', 'w+')
    GAMEOVER_FILE.write('COMPLETE, CONFIGURATION, TIME, STEPS\n')
    ITERATION_TIME = open('IterationTime.cvs', 'w+')
    ITERATION_TIME.write('STEPS, TIME\n')

    mangiato = False
    tic = time.time()

    while run:
        steps = steps + 1
        iter_tic = time.time()

        pygame.time.delay(FRAME_DELAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                file.close()
                GAMEOVER_FILE.close()

        # IRENE: eventualmente eliminare questi metodi e modificare i valori
        # dentro il bot (tenendo un contatore interno del numero di invocazioni)
        player.set_alpha(alpha=0.5)
        player.set_beta(beta=0.5)
        # alpha: snake.length/grid_area s.t. stops greedy algh        
        # beta: snake.length/grid_area s.t. stops dynamic algh

        dir = player.get_next_move()
        
        mangiato = snake.move(dir, food)

        lost = snake.bounds_collision(grid) or \
            snake.tail_collision()

        ham_cycle = {}
        if steps == 1:
            ham_cycle = player.return_cycle(first_step=True)
        else:
            ham_cycle = player.return_cycle(first_step=False)
        
        end = False
        if lost:
            end = True
            text = button.font.render('GAME OVER', True, colors.FUXIA)
            button.window.blit(text, (180, 270))

        if end:
            pygame.display.update()
            pygame.time.delay(700)
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
            if OBSTACLES:
                grid.spawn_obstacles()
            player.update_ham_cycle()
            food.respawn(snakes, grid)
            button.new_game()

        if snake.length == grid.get_grid_free_area():
            toc = time.time()
            grid.draw_cycle(pygame, button.window, ham_cycle, colors.WHITE, closed=True)
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            
            text = button.font.render('COMPLETE', True, colors.FUXIA)
            button.window.blit(text, (180, 270))
            
            iter_toc = time.time()
            steps_time.append(iter_toc - iter_tic)

            pygame.display.update()
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
            
            pygame.display.update()
            pygame.time.delay(700)
            
            steps = 0
            tic = time.time()
            
            snake.respawn(grid)
            if OBSTACLES:
                grid.spawn_obstacles()
                player.update_ham_cycle()                
            food.respawn(snakes, grid)
            button.new_game()
        else:
            if mangiato:
                food.respawn(snakes, grid)
            button.window.fill(colors.BLACK)
            grid.draw_cycle(pygame, button.window, ham_cycle, colors.WHITE, True)
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            food.draw(pygame, button.window, grid)
            pygame.display.update()

def select_start():
    if button.scelta == 'hamilton':
        hamilton_start()
    else:
        singleplayer_start()
        
### nuovo avvio del gioco ###
button.snake_interface()
select_start()