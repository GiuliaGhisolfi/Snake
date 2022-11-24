from enum import Enum
import random as r

class Colors(Enum):
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    ORANGE = (255, 102, 0)
    GREEN = (0, 190, 80)
    BLUE = (0, 0, 255)
    FUXIA = (255, 0, 100)
    PINK = (255, 105, 180)
    RANDOM = (r.randint(0,255), r.randint(0,255), r.randint(0,255))