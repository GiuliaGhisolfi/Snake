from src.player import Player
from src.directions import Directions
import src.grid as grid
import src.food as food
import src.snake as snake
import copy
import time

class Bot(Player):

    def __init__(self, grid, snake, food, config_path, log_path):
        self.grid = grid
        self.snake = snake
        self.food = food
        self.strat = self.strategy
        self.data_to_save = []
        self.parse_config(config_path)
        self.restart_game = True
        self.log_path = log_path
        with open(self.log_path, 'w+') as log:
            log.write('[\n')

    def get_current_grid(self, cells_to_delete):
        #eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(self.grid)
        for segment in cells_to_delete:

            new_grid.delete_cell(segment)
        return new_grid.grid
    
    def set_restart_game(self):
        self.restart_game = True
        
    def reset_restart_game(self):
        self.restart_game = False

    def parse_config(self, file):
        return None

    def strategy(self):
        pass

    def get_next_move(self):
        snake_body_len = len(self.snake.body)
        start_iteration_time = time.time()

        ret = self.strat()

        end_iteration_time = time.time()
        self.data_to_save.append((snake_body_len, end_iteration_time - start_iteration_time))

        return ret

    def save_data(self, last_execution, lost):
        with open(self.log_path, 'a+') as log:
            line = '\t[\n'
            first_iter = True
            for a, b in self.data_to_save:
                if first_iter:
                    line += '\t\t[%.9f,%d]'%(b, a)
                    first_iter  = False
                else:
                    line += ',[%.9f,%d]'%(b, a)
            if not lost:
                line += ',[0,%d]'%(a+1)
            if last_execution:
                line += '\n\t]\n]'
            else:
                line += '\n\t],\n'
            log.write( line )
        
        self.data_to_save = []