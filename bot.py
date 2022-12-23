from player import Player
from directions import Directions
import grid
import food
import snake
import copy
import time

class Bot(Player):

    def __init__(self, grid: grid.Grid, snake: snake.Snake, food:food.Food, config_path, log_path):
        self.grid = grid
        self.snake = snake       
        self.food = food 
        self.strat = self.strategy
        self.data_to_save = []
        self.parse_config(config_path)
        self.log_path = log_path
        with open(self.log_path, 'w') as log:
            log.write('[\n')

    def get_current_grid(self, cells_to_delete):
        #eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(self.grid)
        for segment in cells_to_delete: #manca la testa

            new_grid.delete_cell(segment)
        return new_grid.grid

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

    def save_data(self, last_execution, lost): # TODO: scrivere meglio (flag e last sono brutti...)
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