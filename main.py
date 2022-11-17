import pygame
from concurrent.futures import ThreadPoolExecutor
from grid import Grid
from human_player import HumanPlayer
from bot_twoplayers import Bot_twoplayers
from bot_singleplayer import Bot_singleplayer
from snake import Snake
from food import Food

# colori migliori trovati nel mondo
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 190, 80)
BLUE = (0, 0, 255)
FUXIA = (255, 0, 100)
PINK = (255, 105, 180)

# stat gioco
FRAME_DELAY = 55
X_BLOCKS = 5
Y_BLOCKS = 5

# TODO:
# All'avvio del gioco bisognerebbe creare una finestra e richiedere se si vuole
# giocare in modalità multiplayer o meno.
# Nel primo caso bisogna richiedere se si vogliono scontrare due bot, giocare
# controun bot o giocare contro un altro "HumanPlayer".
# Nel secondo caso  bisogna richiedere se si vuole vedere giocare il bot
# (evetualmente specificando la strategia da fargli adottare, nel caso in cui
# decidiamo di implementarne più di una) o se si vuole giocare dalla tastiera.
# Bisognerebbe anche far scegliere il colore del serpente e i tasti per
# comandarlo.
# E GLI OSTACOLIIIIIIII!!!! importanti :)


def old_start():
    players_info = [
        {
            "type": "bot",
            "color": GREEN,
            "start_location": "top-left",
            "keys": {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN,
                "right": pygame.K_RIGHT,
                "left": pygame.K_LEFT
            }
        },
        {
            "type": "bot",
            "color": BLUE,
            "start_location": "bottom-right",
            "keys": {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN,
                "right": pygame.K_RIGHT,
                "left": pygame.K_LEFT
            }
        }
    ]

    pygame.init()
    grid = Grid(size=700, x_blocks=X_BLOCKS, y_blocks=Y_BLOCKS)
    window = pygame.display.set_mode(grid.bounds)
    pygame.display.set_caption("Snake")
    font = pygame.font.SysFont('Arial', 60, True)

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


def new_start():
    players_info = [
        {
            "type": "sbot",  # human - sbot - mbot
            "color": PINK,
            "start_location": "top-left",

            "keys": {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN,
                "right": pygame.K_RIGHT,
                "left": pygame.K_LEFT
            }
        },
    ]

    pygame.init()
    grid = Grid(size=700, x_blocks=X_BLOCKS, y_blocks=Y_BLOCKS)
    window = pygame.display.set_mode(grid.bounds)
    pygame.display.set_caption("Snake")
    font = pygame.font.SysFont('Arial', 60, True)

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

    food = Food(RED)
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
        elif p["type"] == "sbot":
            player = Bot_singleplayer(grid, snakes[i], food)
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

    # controlli vari
    if players_info[0]['type'] and len(players_info) > 1:
        print('PLAYERS INFO WARNING: using sbot in multiplayer mode')
    if len(players_info) > 1 and players_info[1]['type']:
        print('PLAYERS INFO ERROR: using sbot as second player')

    # avvia il bot corretto
    tasks = []
    for i, p in enumerate(players_info):
        if p['type'] == 'sbot':
            task = pool.submit(players[i].start)

    GAMEOVER_FILE = open('gameOverLog.cvs', 'w+')
    GAMEOVER_FILE.write('CORPO,CIBO\n')

    while run:
        steps = steps + 1

        tasks = []
        for i in range(len(players)):
            if isinstance(players[i], Bot_twoplayers):  # corretto anche con sbot :)
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
                food.respawn(snakes, grid)
            if (players_info[i]['type'] != 'sbot'):
                tasks[i].cancel()

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

                GAMEOVER_FILE.write(str(snakes[0].body))
                GAMEOVER_FILE.write(',')
                GAMEOVER_FILE.write(str(food.position))
                GAMEOVER_FILE.write('\n')
                
                snakes[i].respawn(grid)
            food.respawn(snakes, grid)
            for i in range(len(snakes)):
                if players_info[i]['type'] == 'sbot':
                    players[i].stop()
                    players[i] = Bot_singleplayer(grid, snakes[i], food)

                    task = pool.submit(players[i].start)

            steps = 0

        window.fill(BLACK)
        for i in range(len(snakes)):
            snakes[i].draw(pygame, window, grid)
        food.draw(pygame, window, grid)
        pygame.display.update()

    for i in range(len(players)):
        if players_info[i]['type'] == 'sbot':
            players[i].stop()


new_start()
