from player import Player
from directions import Directions
import grid
import food
import snake
import copy

class Bot(Player):

    def __init__(self, grid: grid.Grid, snake: snake.Snake, food:food.Food):
        self.grid = grid
        self.snake = snake       
        self.food = food 

    def get_current_grid(self, cells_to_delete): # IRENE: possiamo togliere il parametro grid? (non viene mai passato)
        
        #eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(self.grid)
        for segment in cells_to_delete: #manca la testa

            new_grid.delete_cell(segment)
        return new_grid.grid