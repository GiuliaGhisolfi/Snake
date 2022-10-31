from ctypes import windll
from math import floor
from random import random, randrange
import pygame
from snake import *
from food import Food


pygame.init()
x_chessboard = 28
y_chessboard = 25
x_pixel = 700-(700%x_chessboard)
bounds = (x_pixel,x_pixel*y_chessboard/x_chessboard)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake")
block_size = x_pixel/x_chessboard

snake = Snake(block_size, bounds, (0,190,80), x_chessboard, y_chessboard, "user")
bot =  Snake(block_size, bounds, (0, 0, 255), x_chessboard, y_chessboard, "agent")
food = Food(block_size, x_chessboard, y_chessboard, snake.body, bot.body)
font = pygame.font.SysFont('Arial',60, True)

run = True
while run:
  pygame.time.delay(200) #tempo tra un frame e il successivo (in millisecondi)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  
  keys = pygame.key.get_pressed()
  keys_snake = None    
  if keys[pygame.K_UP]:
    keys_snake = 0
  elif keys[pygame.K_DOWN]:
    keys_snake = 1
  elif keys[pygame.K_LEFT]:
    keys_snake = 2
  elif keys[pygame.K_RIGHT]:
    keys_snake = 3
       
  snake.move(keys_snake)
  snake.check_for_food(food, snake.body, bot.body)
    
  keys_bot = randrange(0,4) #algoritmo
  bot.move(keys_bot)
  bot.check_for_food(food, snake.body, bot.body)
  
  
  snake_lost = snake.check_bounds() or snake.check_tail_collision() or snake.check_adversarial_collision(bot)
  bot_lost = bot.check_bounds() or bot.check_tail_collision() or bot.check_adversarial_collision(snake)
  if snake_lost or bot_lost:
      window.fill((0,0,0))
      snake.draw(pygame, window)
      bot.draw(pygame, window)
      
      if snake_lost and bot_lost:
        text = font.render('DRAW', True, (255,0,100))
        window.blit(text, (250,270))  
      elif snake_lost:
        text = font.render('GAME OVER', True, (255,0,100))
        window.blit(text, (180,270))     
      elif bot_lost:
        text = font.render('WIN', True, (255,0,100))
        window.blit(text, (270,270))   
      
      pygame.display.update()
      pygame.time.delay(700) # tempo tra game over e nuova partita
      snake.respawn()
      bot.respawn()
      food.respawn(snake.body, bot.body)
    
  window.fill((0,0,0)) # background
  
  snake.draw(pygame, window)
  bot.draw(pygame, window)
  food.draw(pygame, window)
  pygame.display.update()