from src.bot_player import BotPlayer
from src.directions import Directions

class BotBlind(BotPlayer):
    """This class implements a blind bot, i.e. a bot which chooses moves 
    randomly (it cannot avoid crashing against its body or the frame 
    of the grid)."""

    def get_next_move(self):
        return Directions.random_direction()