from math import floor
from random import random, randrange
import pygame
from snake import *
from food import Food


pygame.init()
x_chessboard = 20
y_chessboard = 20 #per cambiare griglia di gioco cambio questa
x_pixel = 700-(700%x_chessboard)
bounds = (x_pixel,x_pixel*y_chessboard/x_chessboard)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake")
block_size = x_pixel/x_chessboard

snake = Snake(block_size, bounds, (0,190,80), x_chessboard, y_chessboard)
bot =  Snake(block_size, bounds, (0, 0, 255), x_chessboard, y_chessboard)
food = Food(block_size,bounds)
font = pygame.font.SysFont('Arial',60, True)

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
  if snake.check_bounds() or snake.check_tail_collision() or snake.check_adversarial_collision(bot) or \
    bot.check_bounds() or bot.check_tail_collision() or bot.check_adversarial_collision(snake):
      if snake.check_adversarial_collision(bot) and bot.check_adversarial_collision(snake) == True:
        text = font.render('DRAW', True, (255,0,100)) # se le due teste si sovrappongono
        window.blit(text, (250,270))  
      elif snake.check_bounds() or snake.check_tail_collision() or snake.check_adversarial_collision(bot):
        text = font.render('GAME OVER', True, (255,0,100))
        window.blit(text, (180,270))     
      elif bot.check_bounds() or bot.check_tail_collision() or bot.check_adversarial_collision(snake):
        text = font.render('WIN', True, (255,0,100))
        window.blit(text, (270,270))   
      
      pygame.display.update()
      pygame.time.delay(700) ## tempo tra game over e nuova partita
      snake.respawn(x_chessboard, y_chessboard)
      bot.respawn(x_chessboard, y_chessboard)
      food.respawn()
    
  window.fill((0,0,0)) ## background  
  snake.draw(pygame, window)
  bot.draw(pygame, window)
  food.draw(pygame, window)
  pygame.display.update()

