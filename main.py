from math import floor
from random import random, randrange
import pygame
from torch import rand
from snake import *
from food import Food



pygame.init()
x_chessboard = 40
y_chessboard = 34
x_pixel = 700-(700%x_chessboard)
bounds = (x_pixel,x_pixel*y_chessboard/x_chessboard)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake")
block_size = x_pixel/x_chessboard

block_size = 20 ## se si aumenta si rompe e non prende più le mele a meno che non si cambino anche le dimensioni del body dello snake
## le dimensioni devono essere coerenti!!
snake = Snake(block_size, bounds)
bot =  Snake(block_size, bounds)
food = Food(block_size,bounds)
font = pygame.font.SysFont('comicsans',60, True)

run = True
while run:
  pygame.time.delay(200) ##tempo tra un frame e il successivo (in millisecondi)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  
  
  ##################################################################
  #### QUA AGGIORNA LE DIREZIONI IN BASE AI COMANDI DELL'UTENTE ####
  # direzione snake in base ai comandi  
  keys = pygame.key.get_pressed()
  
  # check: se non ho dato indicazioni diverse dalla direzione corrente o opposta, aggiorno la direzione
  if keys[pygame.K_LEFT]: #K_direction è una lista di istruzioni di default di pygame
    snake.steer(Direction.LEFT)
  elif keys[pygame.K_RIGHT]:
    snake.steer(Direction.RIGHT)
  elif keys[pygame.K_UP]:
    snake.steer(Direction.UP)
  elif keys[pygame.K_DOWN]:
    snake.steer(Direction.DOWN)
  ##################################################################
  ##################################################################
       
  snake.move() # mi muovo in base alle direzioni date prima
  snake.check_for_food(food)
  
  keys_bot = randrange(0,4)
  if keys_bot == 0:
    bot.steer(Direction.LEFT)
  elif keys_bot == 1:
    bot.steer(Direction.RIGHT)
  elif keys_bot == 2:
    bot.steer(Direction.UP)
  elif keys_bot == 3:
    bot.steer(Direction.DOWN)
  bot.move()
  bot.check_for_food(food)
  
  ## quando tocco i bordi -> perdo
  if snake.check_bounds() == True or snake.check_tail_collision() == True or \
    bot.check_bounds() == True or bot.check_tail_collision() == True:
      if snake.check_bounds() == True or snake.check_tail_collision() == True:
        text = font.render('Game Over', True, (255,0,100))
      else:
        text = font.render('Win', True, (255,0,100))
  
      window.blit(text, (180,270))
      pygame.display.update()
      pygame.time.delay(700) ## tempo tra game over e nuova partita
      snake.respawn(x_chessboard, y_chessboard)
      bot.respawn(x_chessboard, y_chessboard)
      food.respawn()
  
  ## background  
  window.fill((0,0,0))  ## bianco
  ## nero (0,0,0)
  snake.draw(pygame, window)
  bot.draw(pygame, window)
  food.draw(pygame, window)
  pygame.display.update()

