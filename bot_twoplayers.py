import threading
import random
import copy
from directions import Directions
from player import Player
from search import *
from grid_problem import *
from bot import BotS

# TODO: define a subclass of Problem e.g. GridProblem with an appropriate h

class Bot_twoplayers(BotS):
    def __init__(self, grid):
        self.next_move = None
        self.lock = threading.Lock()
        self.grid = grid
        self.grid = grid.grid
        self.locations = self.build_locations(grid.x_blocks, grid.y_blocks)

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
            self.delete_cell(grid, segment)
        if two_players:
            for i in range(len(adv_snake.body)):
                segment = adv_snake.body[i]
                self.delete_cell(grid, segment)
        
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
            move = self.cell2direction(node.solution()[0], my_head)
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
        return new_grid