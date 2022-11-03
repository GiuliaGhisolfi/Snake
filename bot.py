from random import randrange
from directions import Directions

class Bot():
  def get_next_move(self):
    return Directions(randrange(0, 4))