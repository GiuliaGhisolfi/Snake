import threading
import random
import copy
from directions import Directions
from player import Player
from search import *

# TODO: define a subclass of Problem e.g. GridProblem with an appropriate h

def build_grid(r, c):
    grid = {}
    grid["(0,0)"]={"(0,1)":1, "(1,0)":1}
    grid["(0,%d)"%(c-1)]={"(1,%d)"%(c-1):1, "(0,%d)"%(c-2):1}
    grid["(%d,0)"%(r-1)]={"(%d,0)"%(r-2):1, "(%d,1)"%(r-1):1}
    grid["(%d,%d)"%((r-1),(c-1))]={
        "(%d,%d)"%((r-2),(c-1)):1, 
        "(%d,%d)"%((r-1),(c-2)):1}

    for i in range(c-2):
        grid["(0,%d)"%(i+1)]={
            "(0,%d)"%(i+2):1, 
            "(1,%d)"%(i+1):1, 
            "(0,%d)"%i:1}
        grid["(%d,%d)"%((r-1),(i+1))]={
            "(%d,%d)"%((r-2),(i+1)):1, 
            "(%d,%d)"%((r-1),(i+2)):1, 
            "(%d,%d)"%((r-1),i):1}

    for i in range(r-2):
        grid["(%d,0)"%(i+1)]={
            "(%d,0)"%i:1, 
            "(%d,1)"%(i+1):1, 
            "(%d,0)"%(i+2):1}
        grid["(%d,%d)"%((i+1),(c-1))]={
            "(%d,%d)"%(i,(c-1)):1, 
            "(%d,%d)"%((i+2),(c-1)):1, 
            "(%d,%d)"%((i+1),(c-2)):1}

    for i in range(r-2):
        for j in range(c-2):
            grid["(%d,%d)"%((i+1),(j+1))]={
                "(%d,%d)"%((i),(j+1)):1, 
                "(%d,%d)"%((i+1),(j+2)):1,
                "(%d,%d)"%((i+2),(j+1)):1, 
                "(%d,%d)"%((i+1),(j)):1
            }
    return grid

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

class Bot_two_players(Player):
    def __init__(self, chessboard):
        self.next_move = None
        self.lock = threading.Lock()
        self.chessboard = chessboard
        self.grid = build_grid(chessboard.x_blocks, chessboard.y_blocks)
        self.locations = build_locations(chessboard.x_blocks, chessboard.y_blocks)

    def compute_next_move(self, snakes, my_index, food):
        my_snake = snakes[my_index]
        my_head = my_snake.body[-1]
        bsize = self.chessboard.block_size
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
        self.lock.release()

    def get_next_move(self):
        self.lock.acquire()
        move = self.next_move
        self.lock.release()
        return move