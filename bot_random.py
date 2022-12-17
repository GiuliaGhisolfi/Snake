from bot import Bot
from directions import Directions

class Bot_random(Bot):
    def get_next_move(self):
        possible_dir = self.grid.grid[self.snake.body[-1]]
        if len(possible_dir) > 0:
            return self.snake.dir_to_cell(possible_dir[0])
        else:
            return Directions.random_direction()