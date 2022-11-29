import pygame, sys
from concurrent.futures import ThreadPoolExecutor
from grid import Grid
from human_player import HumanPlayer
from bot_twoplayers import Bot_twoplayers
from bot_singleplayer import Bot_singleplayer
from bot_hamilton import Bot_hamilton
from snake import Snake
from food import Food
from bottoni import *
import colors

# stat gioco, da mettere nel file bottoni per farli modificare a seconda della modalità di gioco

FRAME_DELAY = 5
OBSTACLES = True
# NON MODIFICARE!
X_BLOCKS = 15
Y_BLOCKS = 16
GRID_AREA = X_BLOCKS*Y_BLOCKS
   
pygame.init()
grid = Grid(size=700, x_blocks=X_BLOCKS, y_blocks=Y_BLOCKS)
window = pygame.display.set_mode(grid.bounds)
pygame.display.set_caption("Snake")
font = pygame.font.SysFont('Arial', 40, True)
clock = pygame.time.Clock()

#TODO: separare per bene singleplayer da multiplayer, in modo che:
    #  multiplayer - tenga la threadpool, utilizzi le classi LockedFood e LockedSnake
    #  singleplayer - diventi singlethrea, niente threadpool o cose simili, e che venga gestito
    #               meglio il delay di attesa tra un frame e l'altro perchè sia il max
    #               tra quello scelto e il tempo di esecuzione di get_next_move
mangiato = False
def singleplayer_start():
    players_info = dict_info_single

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
        print(dir, food.fast_get_positions())
        if dir != None:
            
            mangiato = snake.move(dir, food)

            lost = snake.bounds_collision(grid) or \
                snake.tail_collision()

            end = False
            if lost:
                end = True
                text = font.render('GAME OVER', True, colors.FUXIA)
                window.blit(text, (180, 270))
        else:
            text = font.render('LOOP', True, colors.GREEN)
            window.blit(text, (250, 270))
            
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
            
        if end:
            pygame.display.update()
            pygame.time.delay(60000)
            file.write("%s,%s\n" % (snake.length, steps))

            GAMEOVER_FILE.write(str(snake.get_body()))
            GAMEOVER_FILE.write(',')
            GAMEOVER_FILE.write(str(food.position))
            GAMEOVER_FILE.write('\n')
            
            snake.respawn(grid)
            if OBSTACLES: grid.spawn_obstacles()
            food.respawn(snakes, grid)

            steps = 0

        
        if snake.length == GRID_AREA:
            snake.draw(pygame, window, grid)
            grid.draw_obstacles(pygame, window)
            
            text = font.render('COMPLETE', True, colors.FUXIA)
            window.blit(text, (180, 270))
            
            pygame.display.update()
            pygame.time.delay(700)
            
            snake.respawn(grid)
            if OBSTACLES: grid.spawn_obstacles()
            food.respawn(snakes, grid)
        else:
            if mangiato:
                food.respawn(snakes, grid)

            window.fill(colors.BLACK)
            snake.draw(pygame, window, grid)
            grid.draw_obstacles(pygame, window)
            food.draw(pygame, window, grid)
            pygame.display.update()

def hamilton_start():
    players_info = dict_info_single

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
    GAMEOVER_FILE.write('CORPO,CIBO\n')
    
    magiato = False
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


        end = False
        if lost:
            end = True
            text = font.render('GAME OVER', True, colors.FUXIA)
            window.blit(text, (180, 270))

        if end:
            pygame.display.update()
            pygame.time.delay(700)
            file.write("%s,%s\n" % (snake.length, steps))

            GAMEOVER_FILE.write(str(snake.body))
            GAMEOVER_FILE.write(',')
            GAMEOVER_FILE.write(str(food.position))
            GAMEOVER_FILE.write('\n')
            
            snake.respawn(grid)
            if OBSTACLES: grid.spawn_obstacles()
            food.respawn(snakes, grid)

            steps = 0
        
        if snake.length == grid.get_grid_free_area():
            snake.draw(pygame, window, grid)
            grid.draw_obstacles(pygame, window)
            
            text = font.render('COMPLETE', True, colors.FUXIA)
            window.blit(text, (180, 270))
            
            pygame.display.update()
            pygame.time.delay(700)
            
            snake.respawn(grid)
            if OBSTACLES: grid.spawn_obstacles()
            food.respawn(snakes, grid)
        else:
            if mangiato:
                food.respawn(snakes, grid)
            window.fill(colors.BLACK)
            snake.draw(pygame, window, grid)
            grid.draw_obstacles(pygame, window)
            food.draw(pygame, window, grid)
            pygame.display.update()

def multiplayer_start():
    players_info = dict_info

    num_threads = 0
    players = []
    snakes = []
    logfiles = []

    # creo gli snake, poi il cibo e poi il o i bot, necessario per il bot sigleplayer
    for p in players_info:
        snake = Snake(
            color=p["color"],
            start_location=p["start_location"])

        snake.respawn(grid)
        snakes.append(snake)
    
    # creo ostacoli
    #obstacles = Obstacles('gray')
    #obstacles.spawn(snakes, grid)

    food = Food(colors.RED)
    food.respawn(snakes, grid)

    for i, p in enumerate(players_info):  # indice e iteratore nella lista (piccina)
        # logs
        file = open("player"+str(i)+"_logfile.csv", "w")
        file.write("OUTCOME,LENGTH,STEPS\n")
        logfiles.append(file)

        # bots
        if p["type"] == "human":
            player = HumanPlayer(
                game=pygame,
                up_key=p["keys"]["up"],
                down_key=p["keys"]["down"],
                right_key=p["keys"]["right"],
                left_key=p["keys"]["left"])
        elif p["type"] == "mbot":
            player = Bot_twoplayers(grid)
            num_threads = num_threads + 1
        else:
            print('PLAYERS INFO ERROR: player type not recognized')
            exit(1)
        players.append(player)

    pool = None
    if num_threads > 0:
        pool = ThreadPoolExecutor(max_workers=num_threads)

    steps = 0
    run = True

    # avvia il bot corretto
    tasks = []
    GAMEOVER_FILE = open('gameOverLog.cvs', 'w+')
    GAMEOVER_FILE.write('CORPO,CIBO\n')
    
    while run:
        steps = steps + 1

        tasks = []
        for i in range(len(players)):
            if isinstance(players[i], Bot_twoplayers):  
                task = pool.submit(
                    players[i].compute_next_move, snakes, i, food)
                tasks.append(task)

        pygame.time.delay(FRAME_DELAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                for i in range(len(logfiles)):
                    logfiles[i].close()
                    GAMEOVER_FILE.close()

        for i in range(len(players)):
            dir = players[i].get_next_move()
            mangiato = snakes[i].move(dir, food)
            if mangiato: food.respawn(snakes, grid)
                
            if (players_info[i]['type'] != 'sbot' and players_info[i]['type'] != 'human'): #modifica per fa funzionare sbot o human
                tasks[i].cancel()

        lost = []
        for i in range(len(snakes)):
            lost.append(snakes[i].bounds_collision(grid) or
                        snakes[i].tail_collision())

        collisions = []
        collisions.append(
            snakes[0].adversarial_collision(snakes[1].body))
        collisions.append(
            snakes[1].adversarial_collision(snakes[0].body))
        lost[0] = lost[0] or collisions[0]
        lost[1] = lost[1] or collisions[1]
        if collisions[0] or collisions[1]:  # redraw to see which snake collided
            window.fill(colors.BLACK)
            snakes[0].draw(pygame, window, grid)
            snakes[1].draw(pygame, window, grid)

        end = False
        if lost[0] or lost[1]:
            end = True
        if lost[0] and lost[1]:
            text = font.render('DRAW', True, colors.FUXIA)
            window.blit(text, (250, 270))
            logfiles[0].write("DRAW,")
            logfiles[1].write("DRAW,")
        elif lost[0]:
            text = font.render('GAME OVER', True, colors.FUXIA)
            window.blit(text, (180, 230))
            text = font.render('PLAYER 1 WON', True, colors.FUXIA)
            window.blit(text, (140, 310))
            logfiles[0].write("LOST,")
            logfiles[1].write("WIN,")
        elif lost[1]:
            text = font.render('GAME OVER', True, colors.FUXIA)
            window.blit(text, (180, 230))
            text = font.render('PLAYER 1 WON', True, colors.FUXIA)
            window.blit(text, (140, 310))
            logfiles[0].write("WIN,")
            logfiles[1].write("LOST,")

        if end:
            pygame.display.update()
            pygame.time.delay(700)
            for i in range(len(snakes)):
                logfiles[i].write("%s,%s\n" % (snakes[i].length, steps))

                GAMEOVER_FILE.write(str(snakes[0].body))
                GAMEOVER_FILE.write(',')
                GAMEOVER_FILE.write(str(food.position))
                GAMEOVER_FILE.write('\n')
                
                snakes[i].respawn(grid)
            if OBSTACLES: grid.spawn_obstacles()
            food.respawn(snakes, grid)

            steps = 0

        window.fill(colors.BLACK)
        for i in range(len(snakes)):
            snakes[i].draw(pygame, window, grid)
        grid.draw_obstacles(pygame, window)
        food.draw(pygame, window, grid)
        pygame.display.update()

### avvio il gioco ###
if scelta == 'multiplayer':
    multiplayer_start()
elif scelta == 'hamilton':
    hamilton_start()
else:
    singleplayer_start()
