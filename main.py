import pygame, sys
from concurrent.futures import ThreadPoolExecutor
from grid import Grid
from human_player import HumanPlayer
from bot_twoplayers import Bot_twoplayers
from bot_singleplayer import Bot_singleplayer
from bot_hamilton import Bot_hamilton
from snake import Snake
from food import Food
import button
import colors
import directions
import time

FRAME_DELAY = 15
OBSTACLES = True

### NON MODIFICARE!
X_BLOCKS = 15
Y_BLOCKS = 16
#GRID_AREA = X_BLOCKS*Y_BLOCKS
###
pygame.init()
grid = Grid(size=700, x_blocks=X_BLOCKS, y_blocks=Y_BLOCKS)
button.window = pygame.display.set_mode(grid.bounds)
mangiato = False

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
        player = Bot_singleplayer(grid, snakes[0], food, True)
    else:
        print('PLAYERS INFO ERROR: player type not recognized')
        exit(1)

    steps = 0
    run = True

    # avvia il bot corretto
    GAMEOVER_FILE = open('gameOverLog.cvs', 'w+')
    GAMEOVER_FILE.write('CORPO,CIBO\n')

    while run:
        if len(snake.get_body()) != snake.length: print('ops')
        steps = steps + 1

        pygame.time.delay(FRAME_DELAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                file.close()
                GAMEOVER_FILE.close()
   
        dir = player.get_next_move()
        #print(dir, food.fast_get_positions())
        if dir != directions.Directions.CLOSE:
            
            mangiato = snake.move(dir, food)

            lost = snake.bounds_collision(grid) or \
                snake.tail_collision()

            end = False
            if lost:
                end = True
                text = button.font.render('GAME OVER', True, colors.FUXIA)
                button.window.blit(text, (180, 270))

        else:
            text = button.font.render('LOOP', True, colors.GREEN)
            button.window.blit(text, (250, 270))
            
            pygame.display.update()
            pygame.time.delay(700)
            file.write("%s,%s\n" % (snake.length, steps))

            GAMEOVER_FILE.write(str(snake.get_body()))
            GAMEOVER_FILE.write(',')
            GAMEOVER_FILE.write(str(food.position))
            GAMEOVER_FILE.write('\n')
            
            snake.respawn(grid)
            if OBSTACLES: grid.spawn_obstacles()
            food.respawn(snakes, grid)

            steps = 0
            end = False
            button.new_game()
            
        if end:
            pygame.display.update()
            pygame.time.delay(700)
            file.write("%s,%s\n" % (snake.length, steps))

            GAMEOVER_FILE.write(str(snake.get_body()))
            GAMEOVER_FILE.write(',')
            GAMEOVER_FILE.write(str(food.position))
            GAMEOVER_FILE.write('\n')
            
            snake.respawn(grid)
            if OBSTACLES: grid.spawn_obstacles()
            food.respawn(snakes, grid)

            steps = 0
            button.new_game()
        
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
            button.new_game()
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

    mangiato = False
    tic = time.time()

    while run:
        steps = steps + 1

        pygame.time.delay(FRAME_DELAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                file.close()
                GAMEOVER_FILE.close()

        
        dir = player.get_next_move()
        mangiato = snake.move(dir, food)

        lost = snake.bounds_collision(grid) or \
            snake.tail_collision()

        ham_cycle = {}
        ham_cycle = player.return_cycle()
        ham_cycle_changed  = player.return_ham_cycle_changed()
        if steps == 1:
            ham_cycle_changed = True
        
        end = False
        if lost:
            end = True
            text = button.font.render('GAME OVER', True, colors.FUXIA)
            button.window.blit(text, (180, 270))

        if end:
            pygame.display.update()
            pygame.time.delay(700)
            file.write("%s,%s\n" % (snake.length, steps))

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
            grid.draw_cycle(pygame, button.window, ham_cycle, ham_cycle_changed)
            snake.draw(pygame, button.window, grid)
            grid.draw_obstacles(pygame, button.window)
            
            text = button.font.render('COMPLETE', True, colors.FUXIA)
            button.window.blit(text, (180, 270))
            
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
            grid.draw_cycle(pygame, button.window, ham_cycle, ham_cycle_changed)
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