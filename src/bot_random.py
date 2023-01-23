import random
from src.bot_player import BotPlayer
from src.directions import Directions

class BotRandom(BotPlayer):
    """This class implements a bot which chooses to move randomly in one of the 
    free cells adjacent to its head (if any exist)."""

    def get_next_move(self):
        possible_dir = self.grid.grid[self.snake.body[-1]]

        for node in self.snake.body:
            try: possible_dir.remove(node)
            except: pass

        if len(possible_dir) > 0:
            return self.snake.dir_to_cell(
                possible_dir[random.randrange(len(possible_dir))]
            )
        else:
            return Directions.random_direction()