import pygame, sys
from concurrent.futures import ThreadPoolExecutor
from grid import Grid
from human_player import HumanPlayer
from bot_twoplayers import Bot_twoplayers
from bot_singleplayer import Bot_singleplayer
from snake import Snake
from food import Food
from bottoni import *
from obstacles import *

# stat gioco, da mettere nel file bottoni per farli modificare a seconda della modalità di gioco
FRAME_DELAY = 60
X_BLOCKS = 10
Y_BLOCKS = 10
   
pygame.init()
grid = Grid(size=700, x_blocks=X_BLOCKS, y_blocks=Y_BLOCKS)
window = pygame.display.set_mode(grid.bounds)
pygame.display.set_caption("Snake")
font = pygame.font.SysFont('Arial', 40, True)
clock = pygame.time.Clock()
""" funzione deprecata
def old_start():
    players_info = dict_info
    two_players = (len(players_info) == 2)
    num_threads = 0
    players = []
    snakes = []
    logfiles = []
    for i in range(len(players_info)):
        if players_info[i]["type"] == "human":
            player = HumanPlayer(
                game=pygame,
                up_key=players_info[i]["keys"]["up"],
                down_key=players_info[i]["keys"]["down"],
                right_key=players_info[i]["keys"]["right"],
                left_key=players_info[i]["keys"]["left"])
        else:
            player = Bot_twoplayers(grid)
            num_threads = num_threads + 1
        players.append(player)

        file = open("player"+str(i)+"_logfile.csv", "w")
        file.write("OUTCOME,LENGTH,STEPS\n")
        logfiles.append(file)

        snake = Snake(
            color=players_info[i]["color"],
            start_location=players_info[i]["start_location"])
        snake.respawn(grid)
        snakes.append(snake)

    food = Food(RED)
    food.respawn(snakes, grid)
    pool = None
    if num_threads > 0:
        pool = ThreadPoolExecutor(max_workers=num_threads)

    steps = 0
    run = True
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

        for i in range(len(players)):
            dir = players[i].get_next_move()
            tasks[i].cancel()
            snakes[i].move(dir)
            if snakes[i].can_eat(food):
                snakes[i].eat()
                food.respawn(snakes, grid)

        lost = []
        for i in range(len(snakes)):
            lost.append(snakes[i].check_bounds(grid) or
                        snakes[i].check_tail_collision())

        if two_players:
            collisions = []
            collisions.append(
                snakes[0].check_adversarial_collision(snakes[1].body))
            collisions.append(
                snakes[1].check_adversarial_collision(snakes[0].body))
            lost[0] = lost[0] or collisions[0]
            lost[1] = lost[1] or collisions[1]
            if collisions[0] or collisions[1]:  # redraw to see which snake collided
                window.fill(BLACK)
                snakes[0].draw(pygame, window, grid)
                snakes[1].draw(pygame, window, grid)

        end = False
        if two_players:
            if lost[0] or lost[1]:
                end = True
            if lost[0] and lost[1]:
                text = font.render('DRAW', True, FUXIA)
                window.blit(text, (250, 270))
                logfiles[0].write("DRAW,")
                logfiles[1].write("DRAW,")
            elif lost[0]:
                text = font.render('GAME OVER', True, FUXIA)
                window.blit(text, (180, 230))
                text = font.render('PLAYER 1 WON', True, FUXIA)
                window.blit(text, (140, 310))
                logfiles[0].write("LOST,")
                logfiles[1].write("WIN,")
            elif lost[1]:
                text = font.render('GAME OVER', True, FUXIA)
                window.blit(text, (180, 230))
                text = font.render('PLAYER 1 WON', True, FUXIA)
                window.blit(text, (140, 310))
                logfiles[0].write("WIN,")
                logfiles[1].write("LOST,")
        else:
            if lost[0]:
                end = True
                text = font.render('GAME OVER', True, FUXIA)
                window.blit(text, (180, 270))

        if end:
            pygame.display.update()
            pygame.time.delay(700)
            for i in range(len(snakes)):
                logfiles[i].write("%s,%s\n" % (snakes[i].length, steps))
                snakes[i].respawn(grid)
            food.respawn(snakes, grid)
            steps = 0

        window.fill(BLACK)
        for i in range(len(snakes)):
            snakes[i].draw(pygame, window, grid)
        food.draw(pygame, window, grid)
        pygame.display.update()
"""
# TODO: separare per bene singleplayer da multiplayer, in modo che:
    #  multiplayer - tenga la threadpool, utilizzi le classi LockedFood e LockedSnake
    #  singleplayer - diventi singlethrea, niente threadpool o cose simili, e che venga gestito
    #               meglio il delay di attesa tra un frame e l'altro perchè sia il max
    #               tra quello scelto e il tempo di esecuzione di get_next_move

def new_start():
    players_info = dict_info

    two_players = (len(players_info) == 2)
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
    obstacles = Obstacles('gray')
    obstacles.spawn(snakes, grid)

    food = Food(RED)
    food.respawn(snakes, grid, obstacles)

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
        elif p["type"] == "sbot":
            player = Bot_singleplayer(grid, snakes[i], food, obstacles, True)
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
            snakes[i].move(dir)
            if snakes[i].can_eat(food):
                snakes[i].eat()
                food.respawn(snakes, grid, obstacles)
            if (players_info[i]['type'] != 'sbot' and players_info[i]['type'] != 'human'): #modifica per fa funzionare sbot o human
                tasks[i].cancel()

        lost = []
        for i in range(len(snakes)):
            lost.append(snakes[i].check_bounds(grid) or
                        snakes[i].check_tail_collision() or
                        snakes[i].check_obstacles_collision(obstacles))

        if two_players:
            collisions = []
            collisions.append(
                snakes[0].check_adversarial_collision(snakes[1].body))
            collisions.append(
                snakes[1].check_adversarial_collision(snakes[0].body))
            lost[0] = lost[0] or collisions[0]
            lost[1] = lost[1] or collisions[1]
            if collisions[0] or collisions[1]:  # redraw to see which snake collided
                window.fill(BLACK)
                snakes[0].draw(pygame, window, grid)
                snakes[1].draw(pygame, window, grid)

        end = False
        if two_players:
            if lost[0] or lost[1]:
                end = True
            if lost[0] and lost[1]:
                text = font.render('DRAW', True, FUXIA)
                window.blit(text, (250, 270))
                logfiles[0].write("DRAW,")
                logfiles[1].write("DRAW,")
            elif lost[0]:
                text = font.render('GAME OVER', True, FUXIA)
                window.blit(text, (180, 230))
                text = font.render('PLAYER 1 WON', True, FUXIA)
                window.blit(text, (140, 310))
                logfiles[0].write("LOST,")
                logfiles[1].write("WIN,")
            elif lost[1]:
                text = font.render('GAME OVER', True, FUXIA)
                window.blit(text, (180, 230))
                text = font.render('PLAYER 1 WON', True, FUXIA)
                window.blit(text, (140, 310))
                logfiles[0].write("WIN,")
                logfiles[1].write("LOST,")
        else:
            if lost[0]:
                end = True
                text = font.render('GAME OVER', True, FUXIA)
                window.blit(text, (180, 270))

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
            obstacles.spawn(snakes, grid)
            food.respawn(snakes, grid,obstacles)

            steps = 0

        window.fill(BLACK)
        for i in range(len(snakes)):
            snakes[i].draw(pygame, window, grid)
        obstacles.draw(pygame, window, grid)
        food.draw(pygame, window, grid)
        pygame.display.update()

### avvio il gioco ###
new_start()
