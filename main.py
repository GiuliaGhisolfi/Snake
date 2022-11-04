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
PLAYER_1 = "human"
PLAYER_1_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)
PLAYER_2 = "bot"
PLAYER_2_KEYS = (None, None, None, None) # (pygame.K_w, pygame.K_z, pygame.K_s, pygame.K_a)

pygame.init()
chessboard = ChessBoard(size=700, x_blocks=X_BLOCKS, y_blocks=Y_BLOCKS)
window = pygame.display.set_mode(chessboard.bounds)
pygame.display.set_caption("Snake")
font = pygame.font.SysFont('Arial', 60, True)

num_threads = 0
if PLAYER_1 == "human":
    player1 = HumanPlayer(
        pygame, 
        PLAYER_1_KEYS[0], 
        PLAYER_1_KEYS[1], 
        PLAYER_1_KEYS[2], 
        PLAYER_1_KEYS[3])
else:
    player1 = Bot()
    num_threads = num_threads + 1

if PLAYER_2 == "human":
    player2 = HumanPlayer(
        pygame, 
        PLAYER_2_KEYS[0], 
        PLAYER_2_KEYS[1], 
        PLAYER_2_KEYS[2], 
        PLAYER_2_KEYS[3])
else:
    player2 = Bot()
    num_threads = num_threads + 1

player1_logfile = open("player1_logfile.csv", "w")
player2_logfile = open("player2_logfile.csv", "w")
player1_logfile.write("OUTCOME,LENGTH,STEPS\n")
player2_logfile.write("OUTCOME,LENGTH,STEPS\n")
player1_snake = Snake(GREEN, "top-left")
player1_snake.respawn(chessboard)
player2_snake =  Snake(BLUE, "bottom-right")
player2_snake.respawn(chessboard)
food = Food(RED)
food.respawn(player1_snake.body, player2_snake.body, chessboard)
pool = ThreadPoolExecutor(max_workers=num_threads)

steps = 0
run = True
while run:
    steps = steps + 1

    if isinstance(player1, Bot):
        pool.submit(player1.compute_next_move)
    if isinstance(player2, Bot):
        pool.submit(player2.compute_next_move)

    pygame.time.delay(FRAME_DELAY)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            player1_logfile.close()
            player2_logfile.close()
    
    player1_dir = player1.get_next_move()
    player1_snake.move(player1_dir, chessboard)
    if player1_snake.can_eat(food):
        player1_snake.eat()
        food.respawn(player1_snake.body, player2_snake.body, chessboard)

    player2_dir = player2.get_next_move()
    player2_snake.move(player2_dir, chessboard)
    if player2_snake.can_eat(food):
        player2_snake.eat()
        food.respawn(player1_snake.body, player2_snake.body, chessboard)

    player1_lost = player1_snake.check_bounds(chessboard) or \
        player1_snake.check_tail_collision() or \
        player1_snake.check_adversarial_collision(player2_snake.body)
    player2_lost = player2_snake.check_bounds(chessboard) or \
        player2_snake.check_tail_collision() or \
        player2_snake.check_adversarial_collision(player1_snake.body)

    if player1_lost or player2_lost:
        #window.fill(BLACK)
        #player1_snake.draw(pygame, window, chessboard)
        #player2_snake.draw(pygame, window, chessboard)

        if player1_lost and player2_lost:
            text = font.render('DRAW', True, PINK)
            window.blit(text, (250, 270))
            player1_logfile.write("DRAW,")
            player2_logfile.write("DRAW,")
        elif player1_lost:
            text = font.render('GAME OVER', True, PINK)
            window.blit(text, (180, 270))
            player1_logfile.write("LOST,")
            player2_logfile.write("WIN,")
        elif player2_lost:
            text = font.render('WIN', True, PINK)
            window.blit(text, (270, 270))
            player1_logfile.write("WIN,")
            player2_logfile.write("LOST,")
        player1_logfile.write("%s,%s\n"%(player1_snake.length, steps))
        player2_logfile.write("%s,%s\n"%(player2_snake.length, steps))

        pygame.display.update()
        pygame.time.delay(700)
        player1_snake.respawn(chessboard)
        player2_snake.respawn(chessboard)
        food.respawn(player1_snake.body, player2_snake.body, chessboard)
        steps = 0

    window.fill(BLACK)
    player1_snake.draw(pygame, window, chessboard)
    player2_snake.draw(pygame, window, chessboard)
    food.draw(pygame, window, chessboard)
    pygame.display.update()