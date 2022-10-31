from enum import Enum
from random import random, randrange

class Direction(Enum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3


class Snake:

  def __init__(self, block_size, bounds, color, x_chessboard, y_chessboard, player):
    self.block_size = block_size
    self.bounds = bounds
    self.color = color
    self.player = player
    self.x_chessboard = x_chessboard
    self.y_chessboard = y_chessboard
    self.respawn()


  def respawn(self):
    self.length = 3
    if self.player == "user":
      self.body = [(3*self.block_size,2*self.block_size), \
                  (3*self.block_size,3*self.block_size),(3*self.block_size,4*self.block_size)]
      self.direction = Direction.DOWN
    if self.player == "agent":
      self.body = [((self.x_chessboard-4)*self.block_size,(self.y_chessboard-4)*self.block_size), \
                  ((self.x_chessboard-4)*self.block_size,(self.y_chessboard-5)*self.block_size), \
                  ((self.x_chessboard-4)*self.block_size,(self.y_chessboard-6)*self.block_size)]
      self.direction = Direction.UP


  def draw(self, game, window):
    for segment in self.body:
      game.draw.rect(window, self.color, (segment[0], segment[1], self.block_size, self.block_size))


  def move(self, keys):
    if keys == 0:
      self.steer(Direction.UP)
    elif keys == 1:
      self.steer(Direction.DOWN)
    elif keys == 2:
      self.steer(Direction.LEFT)
    elif keys == 3:
      self.steer(Direction.RIGHT)
    
    curr_head = self.body[-1]
    if self.direction == Direction.DOWN:
      next_head = (curr_head[0], curr_head[1] + self.block_size)
      self.body.append(next_head)
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

  def check_for_food(self, food, snake_body, bot_body):
    head = self.body[-1]
    if head[0] == food.x and head[1] == food.y:
      self.eat()
      food.respawn(snake_body, bot_body)


  def check_tail_collision(self):
    head = self.body[-1]
    for i in range(len(self.body) - 1):
      segment = self.body[i]
      if head[0] == segment[0] and head[1] == segment[1]:
        return True
    return False
  
  def check_adversarial_collision(self, adversarial):
    head = self.body[-1]
    for i in range(len(adversarial.body)):
      segment = adversarial.body[i]
      if head[0] == segment[0] and head[1] == segment[1]:
        return True
    return False


  def check_bounds(self):
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
