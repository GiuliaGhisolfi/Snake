import threading
from directions import Directions
from player import Player
from search import *
import copy

import grid
import snake
import food
from grid_problem import *

def get_cycle(n): # n must be even (grid must be square)
    hamcycle = {}
    for i in range(n-1):
        hamcycle[(i, 0)] = i
        hamcycle[(n-1, i)] = n-1+i
        for j in range(n-1):
            if i % 2 == 0:
                hamcycle[(i, j+1)] = n*n-1-(n-1)*i-j
            else:
                hamcycle[(i, j+1)] = n*n-(n-1)*2-(n-1)*(i-1)+j
    hamcycle[(n-1, n-1)] = (n-1)*2
    return hamcycle


def delete_cell(grid, del_key):
    grid.pop(del_key, None)
    for key in grid:
        grid[key].pop(del_key, None)

def coordinates2cell(x, y, bsize):
    return "(%d,%d)" % (x/bsize, y/bsize)

def node2string(x, y):
    return "(%d,%d)" % (x, y)

# restituisce la posizione della cella targhet rispetto alla cella head


def graphDir_to_gameDir(head_pos, target_pos):
    headPosList = head_pos[1:-1].split(',')
    targetPosList = target_pos[1:-1].split(',')

    if int(targetPosList[0]) < int(headPosList[0]):  # x shift
        ret = Directions.LEFT
    elif int(targetPosList[0]) > int(headPosList[0]):
        ret = Directions.RIGHT
    elif int(targetPosList[1]) < int(headPosList[1]):  # y shift
        ret = Directions.UP
    else:
        ret = Directions.DOWN

    return ret


def build_location(grid):
    locations = {}
    for key in grid:
        sL = key.replace('(', '').replace(')', '').split(',')
        locations[key] = (int(sL[0]), int(sL[1]))
    return locations


class Bot_hamilton(Player):
    # input anche lo snake
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food: food.Food):
        self.next_move = Directions.DOWN  # random
        self.grid = grid
        self.locations = build_location(self.grid.grid)  # immutabile

        self.snake = snake
        self.prec_snake_body = self.snake.get_body()

        self.food = food
        # vuota così che dopo start calcola subito
        self.prec_food_position = self.food.get_positions()

        if len(self.prec_snake_body) < 3:
            print('LUNGHEZZA MINIMA SUPPORTATA: 3')
            exit()  # boom

        self.default_path = []
        self.path_to_food = []

        # strategia attuale
        self.chosen_strat = self.hamilton_cicle_start()

    def start(self):
        self.chosen_strat()

    ################# modificare da qua ###############

    def coordinate_from_node(self, node):
        coordinates = node[1:-1].split(',')
        return (int(coordinates[0]), int(coordinates[1]))

    def _relative_dist(self, ori, x, size):
        if ori > x:
            x += size
        return x - ori

    def hamilton_cicle_start(self):
        # prima iterazione va fatta sempre ed è safe, non succedono cose strane
        self.prec_food_position = self.food.get_positions()
        self.prec_snake_body = self.snake.get_body()

        goal = self.get_best_food()
        head = self.prec_snake_body[-1]

        dummy_g = self.get_true_graph(self.prec_snake_body[:-1])
        graph = Graph(dummy_g)
        graph.locations = self.locations

        grid_problem = GridProblem(head, False, goal, graph)
        grid_area = self.grid.x_blocks * self.grid.y_blocks

        ham_cycle = get_cycle(self.grid.x_blocks)
        head_coord = self.coordinate_from_node(head)
        head_ham_pos = ham_cycle[head_coord] # head idx
        for i in ham_cycle.keys():
            if ham_cycle[i]==(head_ham_pos+1):
                move = node2string(i[0], i[1])
        if len(self.snake.get_body()) < 0.5 * grid_area:
            node = astar_search(grid_problem)
            if node != None:
                path_str = node.solution()
                path_coord = self.coordinate_from_node(path_str[0])
                path_ham_pos = ham_cycle[path_coord] # next idx
                tail_coord = self.coordinate_from_node(self.prec_snake_body[0])
                tail_ham_pos = ham_cycle[tail_coord] # tail idx
                food_coord = self.coordinate_from_node(goal)
                food_ham_pos = ham_cycle[food_coord] # food idx
                if not(len(path_str) == 1 and abs(food_ham_pos-tail_ham_pos)):
                    head_rel = self._relative_dist(tail_ham_pos, head_ham_pos, grid_area)
                    path_rel = self._relative_dist(tail_ham_pos, path_ham_pos, grid_area)
                    food_rel = self._relative_dist(tail_ham_pos, food_ham_pos, grid_area)
                    if path_rel > head_rel and path_rel <= food_rel:
                        move = path_str[0]

        self.next_move = graphDir_to_gameDir(head, move)
        """
        self.lock.acquire()
        try:
            self.next_move = graphDir_to_gameDir(head, move)
        finally:
            self.lock.release()
            """

    ########## funzioni default del bot ###################
    def get_best_food(self):
        return self.prec_food_position[0]  # una mela a caso, per ora

    # funzione usata per chiedere la prossima mossa dello snake

    def get_true_graph(self, snake_false_body):
        # eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(self.grid.grid)

        for segment in snake_false_body:
            delete_cell(new_grid, segment)

        return new_grid