from src.player import Player
import copy
import time

class Bot(Player):
    """This class implements a bot which plays Snake."""

    def __init__(self, grid, snake, food, config_path, log_path, test_mode):
        super().__init__()
        self.grid = grid
        self.snake = snake
        self.food = food
        self.strat = self.strategy
        self.data_to_save = []
        self.parse_config(config_path)
        self.log_path = log_path
        if test_mode:
            with open(self.log_path, 'w+') as log:
                log.write('[\n')

    def strategy(self):
        pass

    def parse_config(self, file):
        return None

    def get_next_move(self):
        """Returns next move computed according to a strategy."""
        snake_body_len = len(self.snake.body)
        start_time = time.time()
        ret = self.strat()
        end_time = time.time()
        self.data_to_save.append(
            (end_time - start_time, snake_body_len)
        )
        return ret

    def write_log(self, last_execution, lost):
        """Writes log file."""
        with open(self.log_path, 'a+') as log:
            line = '\t[\n'
            first_iter = True
            for time, len in self.data_to_save:
                if first_iter:
                    line += '\t\t[%.9f,%d]'%(time, len)
                    first_iter  = False
                else:
                    line += ',[%.9f,%d]'%(time, len)
            if not lost:
                line += ',[0,%d]'%(len+1)
            if last_execution:
                line += '\n\t]\n]'
            else:
                line += '\n\t],\n'
            log.write(line)
        
        self.data_to_save = []

    def get_current_grid(self, cells_to_delete):
        """Returns the current game grid (the cells occupied by the snake are
        deleted)."""
        new_grid = copy.deepcopy(self.grid)
        for segment in cells_to_delete:
            new_grid.delete_cell(segment)
        return new_grid.grid