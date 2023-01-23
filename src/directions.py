from enum import Enum
import random as r

class Directions(Enum):
    """This class represents a direction on the game grid."""
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def random_direction():
        return Directions(r.randint(0, 3))