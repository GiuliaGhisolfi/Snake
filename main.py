import pygame
from concurrent.futures import ThreadPoolExecutor
from chessboard import ChessBoard
from human_player import HumanPlayer
from bot import Bot
from snake import Snake
from food import Food

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 190, 80)
BLUE = (0, 0, 255)
PINK = (255, 0, 100)

FRAME_DELAY = 200
X_BLOCKS = 28
Y_BLOCKS = 25

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
chessboard = ChessBoard(size=700, x_blocks=X_BLOCKS, y_blocks=Y_BLOCKS)
window = pygame.display.set_mode(chessboard.bounds)
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
        player = Bot(chessboard)
        num_threads = num_threads + 1
    players.append(player)

    file = open("player"+str(i)+"_logfile.csv", "w")
    file.write("OUTCOME,LENGTH,STEPS\n")
    logfiles.append(file)
    
    snake = Snake(
        color=players_info[i]["color"], 
        start_location=players_info[i]["start_location"])
    snake.respawn(chessboard)
    snakes.append(snake)

food = Food(RED)
food.respawn(snakes, chessboard)
pool = None
if num_threads > 0:
    pool = ThreadPoolExecutor(max_workers=num_threads)

steps = 0
run = True
while run:
    steps = steps + 1

    tasks = []
    for i in range(len(players)):
        if isinstance(players[i], Bot):
            task = pool.submit(players[i].compute_next_move, snakes, i, food)
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
        snakes[i].move(dir, chessboard)
        if snakes[i].can_eat(food):
            snakes[i].eat()
            food.respawn(snakes, chessboard)

    lost = []
    for i in range(len(snakes)):
        lost.append(snakes[i].check_bounds(chessboard) or \
            snakes[i].check_tail_collision())

    if two_players:
        collisions = []
        collisions.append(snakes[0].check_adversarial_collision(snakes[1].body))
        collisions.append(snakes[1].check_adversarial_collision(snakes[0].body))
        lost[0] = lost[0] or collisions[0]
        lost[1] = lost[1] or collisions[1]
        if collisions[0] or collisions[1]: # redraw to see which snake collided
            window.fill(BLACK)
            snakes[0].draw(pygame, window, chessboard)
            snakes[1].draw(pygame, window, chessboard)

    end = False
    if two_players:
        if lost[0] or lost[1]:
            end = True
        if lost[0] and lost[1]:
            text = font.render('DRAW', True, PINK)
            window.blit(text, (250, 270))
            logfiles[0].write("DRAW,")
            logfiles[1].write("DRAW,")
        elif lost[0]:
            text = font.render('GAME OVER', True, PINK)
            window.blit(text, (180, 230))
            text = font.render('PLAYER 1 WON', True, PINK)
            window.blit(text, (140, 310))
            logfiles[0].write("LOST,")
            logfiles[1].write("WIN,")
        elif lost[1]:
            text = font.render('GAME OVER', True, PINK)
            window.blit(text, (180, 230))
            text = font.render('PLAYER 1 WON', True, PINK)
            window.blit(text, (140, 310))
            logfiles[0].write("WIN,")
            logfiles[1].write("LOST,")
    else:
        if lost[0]:
            end = True
            text = font.render('GAME OVER', True, PINK)
            window.blit(text, (180, 270))

    if end:
        pygame.display.update()
        pygame.time.delay(700)
        for i in range(len(snakes)):
            logfiles[i].write("%s,%s\n"%(snakes[i].length, steps))
            snakes[i].respawn(chessboard)
        food.respawn(snakes, chessboard)
        steps = 0

    window.fill(BLACK)
    for i in range(len(snakes)):
        snakes[i].draw(pygame, window, chessboard)
    food.draw(pygame, window, chessboard)
    pygame.display.update()