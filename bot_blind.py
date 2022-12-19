from bot import Bot
from directions import Directions

class Bot_blind(Bot):
    def get_next_move(self):
        return Directions.random_direction()