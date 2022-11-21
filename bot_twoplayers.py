import threading
import random
import copy
from directions import Directions
from my_a_star import My_a_star
from player import Player
from search import *
from grid_problem import *

# TODO: define a subclass of Problem e.g. GridProblem with an appropriate h


def build_locations(r, c):
    locations = {}
    for i in range(r):
        for j in range(c):
            locations["(%d,%d)"%(i,j)]=(i,j)
    return locations

def delete_cell(grid, del_key):
    grid.pop(del_key, None)
    for key in grid.keys():
        grid[key].pop(del_key, None)

def cell2direction(grid_position, curr_position):
        positions = curr_position[1:-1].split(',')
        x_curr = int(positions[0])
        y_curr = int(positions[1])
        positions = grid_position[1:-1].split(',')
        x_new = int(positions[0])
        y_new = int(positions[1])
        if x_new > x_curr:
            return Directions.RIGHT
        elif x_new < x_curr:
            return Directions.LEFT
        elif y_new < y_curr:
            return Directions.UP
        else:
            return Directions.DOWN

class Bot_twoplayers(Player):
    def __init__(self, grid, obstacles):
        self.next_move = None
        self.lock = threading.Lock()
        self.grid = grid
        self.grid = grid.grid
        self.locations = build_locations(grid.x_blocks, grid.y_blocks)
        self.obstacles = obstacles

    def compute_next_move(self, snakes, my_index, food):
        my_snake = snakes[my_index]
        my_head = my_snake.body[-1] 
        grid = copy.deepcopy(self.grid)
        two_players = False
        if len(snakes) > 1:
            two_players = True
            adv_index = 1 if my_index == 0 else 0
            adv_snake = snakes[adv_index]
        
        # Update the grid
        for i in range(len(my_snake.body)-1):
            segment = my_snake.body[i]
            delete_cell(grid, segment)
        if two_players:
            for i in range(len(adv_snake.body)):
                segment = adv_snake.body[i]
                delete_cell(grid, segment)
        
        grid = self.get_true_graph(grid)
        
        # Compute the optimal path to the food
        # TODO: avoid computing it each time from scratch
        graph = Graph(grid)
        graph.locations = self.locations
        start = my_head
        goal = food.position[0]
        grid_problem = GridProblem(start, False, goal, graph)
        node = astar_search(grid_problem) # A* con Manhattan Distance
        move = None
        if node != None:
            move = cell2direction(node.solution()[0], my_head)
        # else: TODO:
        #   move = non fatal move

        self.lock.acquire()
        self.next_move = move
        self.lock.release()

    def get_next_move(self):
        self.lock.acquire()
        move = self.next_move
        self.lock.release()
        return move

    def get_true_graph(self, grid={}):
        if not grid:
            grid = self.grid.grid # da controllare

        #eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(grid)

        for pos in self.obstacles.positions:
            str_pos = "(%d,%d)" % (pos[0], pos[1])
            delete_cell(new_grid, str_pos)
        return new_grid