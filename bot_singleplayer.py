import threading
from directions import Directions
from player import Player
from search import *
import copy

import grid
import snake
import food


def delete_cell(grid, del_key):
    grid.pop(del_key, None)
    for key in grid.keys():
        grid[key].pop(del_key, None)


def coordinates2cell(x, y, bsize):
    return "(%d,%d)" % (x/bsize, y/bsize)


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

    if tagerPosList[0] != headPosList[0]:  # x shift
        if tagerPosList[0] < headPosList[0]:
            return Directions.LEFT
        else:
            return Directions.RIGHT
    else:  # y shift
        if tagerPosList[1] < headPosList[1]:
            return Directions.UP
        else:
            return Directions.DOWN





class Bot_singleplayer(Player):
    # input anche lo snake
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food:food.Food):
        self.lock = threading.Lock() #per default path
        self.condition = threading.Condition(self.lock) #variabile di condizione
        self.next_move = Directions.LEFT #random
        self.grid = grid
        self.snake = snake


        self.food = food
        self.prec_food_position = [self.food.get_positions()] #vuota così che dopo start calcola subito
        
        if len(self.snake.body) < 3:
            print('LUNGHEZZA MINIMA SUPPORTATA: 3')
            exit() #boom

        self.default_path = []
        self.path_to_food = []

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
        # prima iterazione va fatta sempre
        move = self.default_path[0] # la mossa è stata presa, aggiorniamo
        self.default_path.pop()
        self.default_path.append(move)


        goal = self.get_best_food()
        start = self.snake.body[-1]

        graph = Graph(self.get_true_graph())
        grid_problem = GraphProblem(start, goal, graph)
        # modificare con la nuova euristica
        computed_path_toFood = astar_search(grid_problem) #esiste il primo, per forza

        #ora calcoliamo dalla mela alla coda
        #aggiornando il grafo con la posizione futura
        next_pos = computed_path_toFood[-len(self.snake.body + 1):]
        goal = next_pos[0] #futura coda
        start = next_pos[-1] #futura testa
        graph = Graph(self.get_true_graph())
        grid_problem = GraphProblem(start, goal, graph)
        computed_cicle = astar_search(grid_problem) #esiste il primo, per forza

        self.default_path = computed_cicle + next_pos[1:] #ciclo privo di rischi
        self.path_to_food = computed_path_toFood #path verso la mela, da percorrere prima di usare default path

        while not self.termination:
            self.lock.acquire()
            self.condition.wait() # soltanto per capire quando controllare se default path ancora buono
            
            
            move = self.default_path[0] # la mossa è stata presa, aggiorniamo
            self.default_path.pop()
            self.default_path.append(move)
            
            self.lock.release()

            # controlliamo se il default path è ok, se non è così rese
            
            

            if self.prec_food_position != self.food.get_positions():
                pass
            
        
    def get_best_food(self):
        return self.prec_food_position[0] #una mela a caso, per ora

    def stop(self):
        self.termination = True
    
    # funzione usata per chiedere la prossima mossa dello snake
    def get_next_move(self):
        self.lock.acquire()
        try:
            move = self.next_move
            self.next_move = None #confermare che la mossa è stata presa
            self.condition.notify()
        finally: self.lock.release()
        return graphDir_to_gameDir(move)

    def get_true_graph(self):
    #eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(self.grid.grid)

        for segment in self.snake.body[1:-1]:
            delete_cell(new_grid, segment)

        return new_grid
