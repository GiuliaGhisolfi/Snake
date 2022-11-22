import threading
from directions import Directions
from player import Player
from search import *
import copy

import grid
import snake
import food
from grid_problem import *


def delete_cell(grid, del_key):
    grid.pop(del_key, None)
    for key in grid:
        grid[key].pop(del_key, None)


def coordinates2cell(x, y, bsize):
    return "(%d,%d)" % (x/bsize, y/bsize)

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


def next_direc(self, snake):
    head = snake.position[-1]  # sistemare da qua
    nxt_direc = self._table[head.x][head.y].direc

    # Take shorcuts when the snake is not too long
    if self._shortcuts and self.snake.len() < 0.5 * self.map.capacity:
        path = self._path_solver.shortest_path_to_food()
        if path:
            tail, nxt, food = self.snake.tail(), head.adj(
                path[0]), self.map.food
            tail_idx = self._table[tail.x][tail.y].idx
            head_idx = self._table[head.x][head.y].idx
            nxt_idx = self._table[nxt.x][nxt.y].idx
            food_idx = self._table[food.x][food.y].idx
            # Exclude one exception
            if not (len(path) == 1 and abs(food_idx - tail_idx) == 1):
                head_idx_rel = self._relative_dist(
                    tail_idx, head_idx, self.map.capacity)
                nxt_idx_rel = self._relative_dist(
                    tail_idx, nxt_idx, self.map.capacity)
                food_idx_rel = self._relative_dist(
                    tail_idx, food_idx, self.map.capacity)
                if nxt_idx_rel > head_idx_rel and nxt_idx_rel <= food_idx_rel:
                    nxt_direc = path[0]

    return nxt_direc


def _relative_dist(self, ori, x, size):
    # copiata, può essere utile
    if ori > x:
        x += size
    return x - ori


def build_location(grid):
    locations = {}
    for key in grid:
        sL = key.replace('(', '').replace(')', '').split(',')
        locations[key] = (int(sL[0]), int(sL[1]))
    return locations


class Bot_singleplayer(Player):
    # input anche lo snake
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food: food.Food):
        self.lock = threading.Lock()  # per default path
        self.condition = threading.Condition(
            self.lock)  # variabile di condizione
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

        # se True termina il thread
        self.termination = False

        # strategia attuale
        self.chosen_strat = self.hamilton_cicle_start

    def start(self):
        self.chosen_strat()

    ################# modificare da qua ###############

    def hamilton_cicle_start(self):
        # prima iterazione va fatta sempre ed è safe, non succedono cose strane
        self.prec_food_position = self.food.get_positions()
        self.prec_snake_body = self.snake.get_body()

        goal = self.get_best_food()
        start = self.prec_snake_body[-1]

        dummy_g = self.get_true_graph(self.prec_snake_body[:-1])
        graph = Graph(dummy_g)
        graph.locations = self.locations

        grid_problem = GridProblem(start, False, goal, graph)
        grid_area = self.grid.x_blocks * self.grid.y_blocks

        # se siamo arrivati qui allora, abbiamo 2 percorsi
        self.lock.acquire()
        try:
            if self.next_move != None:  # abbiamo fatto in tempo !!!
                move = self.path_to_food.pop(0)
                self.next_move = graphDir_to_gameDir(
                    self.prec_snake_body[-1], move)
                # TODO: aggiungere un meccanismo di recupero, magari aspettando un giro intero???
            else:  # siamo stati lenti, aiai
                move = self.default_path.pop(0)
                self.next_move = graphDir_to_gameDir(
                    self.prec_snake_body[-1], move)  # è un ciclo
                self.default_path.append(move)

                skipWait = True
        finally:
            self.lock.release()

    ########## funzioni default del bot ###################
    def get_best_food(self):
        return self.prec_food_position[0]  # una mela a caso, per ora

    def stop(self):
        self.termination = True
        self.lock.acquire()
        self.condition.notify(1)
        self.lock.release()

    # funzione usata per chiedere la prossima mossa dello snake

    def get_next_move(self):
        self.lock.acquire()
        try:
            move = self.next_move
            self.next_move = None  # confermare che la mossa è stata presa
            self.condition.notify(1)
        finally:
            self.lock.release()

        return move

    def get_true_graph(self, snake_false_body):
        # eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(self.grid.grid)

        for segment in snake_false_body:
            delete_cell(new_grid, segment)

        return new_grid
