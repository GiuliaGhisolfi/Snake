import threading
import random
import copy
from directions import Directions
from player import Player
from search import *
from grid_problem import *
from bot import BotS

class Bot_twoplayers(BotS):
    def __init__(self, grid):
        self.next_move = None
        self.lock = threading.Lock()
        self.grid = grid.grid

    def compute_next_move(self, snakes, my_index, food):
        my_snake = snakes[my_index]
        my_head = my_snake.body[-1] 
        grid = copy.deepcopy(self.grid)
        two_players = False
        if len(snakes) > 1:
            two_players = True
            adv_index = 1 if my_index == 0 else 0
            adv_snake = snakes[adv_index]
        
        # Update the grid (like get true graph)
        for i in range(len(my_snake.body)-1):
            segment = my_snake.body[i]
            self.delete_cell(grid, segment)
        if two_players:
            for i in range(len(adv_snake.body)):
                segment = adv_snake.body[i]
                self.delete_cell(grid, segment)
        
        start = my_head
        goal = food.position[0]
        grid_problem = GridProblem(start, goal, grid, False)
        node = astar_search(grid_problem)
        move = None
        if node != None:
            move = self.graphDir_to_gameDir(my_head, node.solution()[0])
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