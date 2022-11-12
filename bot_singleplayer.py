import threading
from directions import Directions
from player import Player
from search import *

import grid
import snake

def delete_cell(grid, del_key):
    grid.pop(del_key, None)
    for key in grid.keys():
        grid[key].pop(del_key, None)

def coordinates2cell(x, y, bsize):
    return "(%d,%d)"%(x/bsize, y/bsize)

def cell2direction(grid_position, x_curr, y_curr, bsize):
        positions = grid_position[1:-1].split(',')
        x_new = int(positions[0])*bsize
        y_new = int(positions[1])*bsize
        if x_new > x_curr:
            return Directions.RIGHT
        elif x_new < x_curr:
            return Directions.LEFT
        elif y_new < y_curr:
            return Directions.UP
        else:
            return Directions.DOWN

# restituisce la posizione della cella targhet rispetto alla cella head
def graphDir_to_gameDir(head_pos, target_pos):
    headPosList = head_pos[1:-1].split(',')
    tagerPosList = target_pos[1:-1].split(',')

    if tagerPosList[0] != headPosList[0]: # x shift
        if tagerPosList[0] < headPosList[0]: return Directions.LEFT
        else: return Directions.RIGHT
    else: # y shift
        if tagerPosList[1] < headPosList[1]: return Directions.UP
        else: return Directions.DOWN

class Bot_singleplayer(Player):
    # input anche lo snake
    def __init__(self, grid: grid.Grid, snake:snake.Snake):
        self.lock = threading.Lock()

        self.grid = grid
        self.snake = snake


        graph = Graph(self.grid.grid) 
        graph.locations = self.grid.locations

        # definiamo il percorso default da seguire come un ciclo testa-coda-testa (siamo piccini non ci schiantiamo)
        start = snake.body[-1] # errore fino a quando snake non viene aggiornato
        goal = snake.bosy[0]
        grid_problem = GraphProblem(start, goal, graph)
        computed_path = astar_search(grid_problem) # modificare con la nuova euristica
        computed_path += snake.body[1:]

        self.default_path = computed_path

        # se True termina il thread
        self.termination = False

    '''
    def compute_next_move(self, snakes, my_index, food):
        my_snake = snakes[my_index]
        my_head = my_snake.body[-1]
        bsize = self.grid.block_size
        grid = copy.deepcopy(self.grid)
        two_players = False
        if len(snakes) > 1:
            two_players = True
            adv_index = 1 if my_index == 0 else 0
            adv_snake = snakes[adv_index]
        
        # Update the grid
        for i in range(len(my_snake.body)-1):
            segment = my_snake.body[i]
            key = coordinates2cell(segment[0], segment[1], bsize)
            delete_cell(grid, key)
        if two_players:
            for i in range(len(adv_snake.body)):
                segment = adv_snake.body[i]
                key = coordinates2cell(segment[0], segment[1], bsize)
                delete_cell(grid, key)
        
        # Compute the optimal path to the food
        # TODO: avoid computing it each time from scratch
        graph = Graph(grid)
        graph.locations = self.locations
        start = coordinates2cell(my_head[0], my_head[1], bsize)
        goal = coordinates2cell(food.x, food.y, bsize)
        grid_problem = GraphProblem(start, goal, graph)
        node = astar_search(grid_problem) # default h = euclidean distance, Manhattan distance is better...
        move = None
        if node != None:
            move = cell2direction(node.solution()[0], my_head[0], my_head[1], bsize)
        # else: TODO:
        #   move = non fatal move

        self.lock.acquire()
        self.next_move = move
        self.lock.release()'''


    # IMPLEMENTARE
    def start(self):
        return
    def stop(self):
        self.termination = True

    def get_next_move(self):
        self.lock.acquire()

        move = self.default_path[0]
        self.default_path.pop()
        self.default_path.append(move)
        self.lock.release()
        return graphDir_to_gameDir(move)