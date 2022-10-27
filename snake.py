from enum import Enum
from random import random, randrange

class Direction(Enum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3


class Snake:
  length = None
  direction = None
  body = None
  block_size = None
  bounds = None


  def __init__(self, block_size, bounds, color, x_chessboard, y_chessboard):
    self.block_size = block_size
    self.bounds = bounds
    self.color = color
    self.respawn(x_chessboard, y_chessboard)


  def respawn(self, x_chessboard, y_chessboard):
    self.length = 3
    # partono tutti gli snake nella stessa posizione
    x_number = randrange(4, x_chessboard-4)
    y_number = randrange(4, y_chessboard-4)
    self.body = [(x_number*self.block_size,y_number*self.block_size), \
                 (x_number*self.block_size,(y_number+1)*self.block_size),(x_number*self.block_size,(y_number+2)*self.block_size)]
    self.direction = Direction.DOWN


  def draw(self, game, window):
    for segment in self.body:
      game.draw.rect(window, self.color, (segment[0],segment[1],self.block_size, self.block_size))


  def move(self):
    # definisco dove mi muovo in base ai comandi
    curr_head = self.body[-1] ## def. testa di questa iterazione
    if self.direction == Direction.DOWN:
      next_head = (curr_head[0], curr_head[1] + self.block_size)
      self.body.append(next_head) ## aggiungo la testa nuova
    elif self.direction == Direction.UP:
      next_head = (curr_head[0], curr_head[1] - self.block_size)
      self.body.append(next_head)
    elif self.direction == Direction.RIGHT:
      next_head = (curr_head[0] + self.block_size, curr_head[1])
      self.body.append(next_head)
    elif self.direction == Direction.LEFT:
      next_head = (curr_head[0] - self.block_size, curr_head[1])
      self.body.append(next_head)

    if self.length < len(self.body):
      self.body.pop(0)


  def steer(self, direction):
    # controlla che io abbia dato un indicazione coerente
    if self.direction == Direction.DOWN and direction != Direction.UP:
      self.direction = direction
    elif self.direction == Direction.UP and direction != Direction.DOWN:
      self.direction = direction
    elif self.direction == Direction.LEFT and direction != Direction.RIGHT:
      self.direction = direction
    elif self.direction == Direction.RIGHT and direction != Direction.LEFT:
      self.direction = direction


  def eat(self):
    self.length += 1

  def check_for_food(self, food):
    head = self.body[-1]
    if head[0] == food.x and head[1] == food.y:
      self.eat() ## allunga snake quando mangia
      food.respawn() ## fa riapparire mele in una posizione random


  def check_tail_collision(self):
    #TODO: questa funzione si può ottimizzare mettendola in check_adversarial_collision(self, self)
    head = self.body[-1]
    has_eaten_tail = False

    for i in range(len(self.body) - 1):
      segment = self.body[i]
      ## controllo se le cordinate della testa è nella stessa posizione del corpo
      if head[0] == segment[0] and head[1] == segment[1]:
        has_eaten_tail = True

    return has_eaten_tail
  
  def check_adversarial_collision(self, adversarial):
    head = self.body[-1]
    for i in range(len(adversarial.body)):
      segment = adversarial.body[i]
      if head[0] == segment[0] and head[1] == segment[1]:
        return True
    return False


  def check_bounds(self):
    ## cotrollo che le coordinate della testa siano interne alla griglia di gioco
    head = self.body[-1]
    if head[0] >= self.bounds[0]:
      return True
    if head[1] >= self.bounds[1]:
      return True

    if head[0] < 0:
        return True
    if head[1] < 0:
        return True

    return False
