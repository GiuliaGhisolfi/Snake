import pygame
from concurrent.futures import ThreadPoolExecutor
from bot import Bot
from snake import Snake
from food import Food
from directions import Directions

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 190, 80)
BLUE = (0, 0, 255)
PINK = (255, 0, 100)

pygame.init()
x_chessboard = 28
y_chessboard = 25
x_pixel = 700-(700%x_chessboard)
bounds = (x_pixel, x_pixel*y_chessboard/x_chessboard)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake")
block_size = x_pixel/x_chessboard
bot = Bot()
human_snake = Snake(block_size, bounds, GREEN, "user")
human_snake.respawn(x_chessboard, y_chessboard)
bot_snake =  Snake(block_size, bounds, BLUE, "agent")
bot_snake.respawn(x_chessboard, y_chessboard)
food = Food(RED, block_size, x_chessboard, y_chessboard, human_snake.body, bot_snake.body)
font = pygame.font.SysFont('Arial', 60, True)

with ThreadPoolExecutor(max_workers=2) as ex:
  run = True
  while run:
    future = ex.submit(bot.get_next_move)

    pygame.time.delay(200) #tempo tra un frame e il successivo (in millisecondi)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
    
    keys = pygame.key.get_pressed()
    human_dir = None
    if keys[pygame.K_UP]:
      human_dir = Directions.UP
    elif keys[pygame.K_DOWN]:
      human_dir = Directions.DOWN
    elif keys[pygame.K_LEFT]:
      human_dir = Directions.LEFT
    elif keys[pygame.K_RIGHT]:
      human_dir = Directions.RIGHT
        
    human_snake.move(human_dir)
    human_snake.check_for_food(food, human_snake.body, bot_snake.body)

    bot_dir = None
    if future.done():
      bot_dir = future.result()
    else:
      future.cancel() # il task viene cancellato se non è ancora stato avviato
    
    bot_snake.move(bot_dir)
    bot_snake.check_for_food(food, human_snake.body, bot_snake.body)
    
    human_lost = human_snake.check_bounds() or human_snake.check_tail_collision() or human_snake.check_adversarial_collision(bot_snake)
    bot_lost = bot_snake.check_bounds() or bot_snake.check_tail_collision() or bot_snake.check_adversarial_collision(human_snake)
    if human_lost or bot_lost:
        window.fill(BLACK)
        human_snake.draw(pygame, window)
        bot_snake.draw(pygame, window)
        
        if human_lost and bot_lost:
          text = font.render('DRAW', True, PINK)
          window.blit(text, (250, 270))
        elif human_lost:
          text = font.render('GAME OVER', True, PINK)
          window.blit(text, (180, 270))
        elif bot_lost:
          text = font.render('WIN', True, PINK)
          window.blit(text, (270, 270))
        
        pygame.display.update()
        pygame.time.delay(700) # tempo tra game over e nuova partita
        human_snake.respawn(x_chessboard, y_chessboard)
        bot_snake.respawn(x_chessboard, y_chessboard)
        food.respawn(human_snake.body, bot_snake.body)
      
    window.fill(BLACK) # background
    
    human_snake.draw(pygame, window)
    bot_snake.draw(pygame, window)
    food.draw(pygame, window)
    pygame.display.update()