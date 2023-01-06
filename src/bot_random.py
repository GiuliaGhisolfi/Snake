from src.bot import Bot
from src.directions import Directions
import random

class Bot_random(Bot):
    def get_next_move(self):
        possible_dir = self.grid.grid[self.snake.body[-1]]

        for node in self.snake.body:
            try: possible_dir.remove(node)
            except: pass

        if len(possible_dir) > 0:
            return self.snake.dir_to_cell(possible_dir[random.randrange(len(possible_dir))])
        else:
            return Directions.random_direction()