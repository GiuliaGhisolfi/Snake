from directions import Directions

class Snake:

  def __init__(self, block_size, bounds, color, player):
    self.block_size = block_size
    self.bounds = bounds
    self.color = color
    self.player = player


  def respawn(self, x_chessboard, y_chessboard):
    self.length = 3
    if self.player == "user":
      self.body = [(3*self.block_size,2*self.block_size), \
                  (3*self.block_size,3*self.block_size),(3*self.block_size,4*self.block_size)]
      self.direction = Directions.DOWN
    if self.player == "agent":
      self.body = [((x_chessboard-4)*self.block_size,(y_chessboard-4)*self.block_size), \
                  ((x_chessboard-4)*self.block_size,(y_chessboard-5)*self.block_size), \
                  ((x_chessboard-4)*self.block_size,(y_chessboard-6)*self.block_size)]
      self.direction = Directions.UP


  def draw(self, game, window):
    for segment in self.body:
      game.draw.rect(window, self.color, (segment[0], segment[1], self.block_size, self.block_size))


  def move(self, direction):
    self.steer(direction)
    
    curr_head = self.body[-1]
    if self.direction == Directions.DOWN:
      next_head = (curr_head[0], curr_head[1] + self.block_size)
      self.body.append(next_head)
    elif self.direction == Directions.UP:
      next_head = (curr_head[0], curr_head[1] - self.block_size)
      self.body.append(next_head)
    elif self.direction == Directions.RIGHT:
      next_head = (curr_head[0] + self.block_size, curr_head[1])
      self.body.append(next_head)
    elif self.direction == Directions.LEFT:
      next_head = (curr_head[0] - self.block_size, curr_head[1])
      self.body.append(next_head)

    if self.length < len(self.body):
      self.body.pop(0)


  def steer(self, direction):
    if direction == None:
      return
    if self.direction == Directions.DOWN and direction != Directions.UP:
      self.direction = direction
    elif self.direction == Directions.UP and direction != Directions.DOWN:
      self.direction = direction
    elif self.direction == Directions.LEFT and direction != Directions.RIGHT:
      self.direction = direction
    elif self.direction == Directions.RIGHT and direction != Directions.LEFT:
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
