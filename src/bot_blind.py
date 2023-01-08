from src.bot import Bot
from src.directions import Directions

class Bot_blind(Bot):
    """This class implements a blind bot, i.e. a bot which chooses moves 
    randomly (it cannot avoid crashing against its body or the frame 
    of the grid)."""

    def get_next_move(self):
        return Directions.random_direction()