from enum import Enum
import random as r

class Directions(Enum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3

  CLOSE = -1

  def random_direction():
    return r.randint(0, 3)


