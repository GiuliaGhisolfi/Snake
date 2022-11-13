import threading
from directions import Directions
from player import Player
from search import *
import copy

import grid
import snake
import food
from grid_problem import GridProblem

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

def build_location(grid):
    locations = {}
    for key in grid:
        sL = key.replace('(', '').replace(')','').split(',')
        locations[key]=(int(sL[0]), int(sL[1]))
    return locations


class Bot_singleplayer(Player):
    # input anche lo snake
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food:food.Food):
        self.lock = threading.Lock() #per default path
        self.condition = threading.Condition(self.lock) #variabile di condizione
        self.next_move = Directions.DOWN #random
        self.grid = grid
        self.locations = build_location(self.grid.grid)
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

        #strategia attuale
        self.chosen_strat = self.mela_cicle_strat


    
    def start(self):
        self.chosen_strat()
            

    def mela_cicle_strat(self):
        # prima iterazione va fatta sempre ed è safe, non succedono cose strane

        self.prec_food_position = self.food.get_positions()
        goal = self.get_best_food()
        start = self.snake.body[-1]

        dummy_g = self.get_true_graph(self.snake.body)
        graph = Graph(dummy_g) 
        graph.locations = self.locations

        grid_problem = GridProblem(start, goal, graph)
        computed_path_toFood = astar_search(grid_problem).solution() #esiste il primo, per forza

        #ora calcoliamo dalla mela alla coda
        #aggiornando il grafo con la posizione futura
        next_pos = (self.snake.body + computed_path_toFood)[-len(self.snake.body) - 1:]
        goal = next_pos[0] #futura coda
        start = next_pos[-1] #futura testa

        dummy_g = self.get_true_graph(next_pos)
        graph = Graph(dummy_g) 
        graph.locations = self.locations
        grid_problem = GridProblem(start, goal, graph)
        computed_cicle = astar_search(grid_problem).solution() #esiste il primo, per forza

        self.default_path = computed_cicle + next_pos[1:] #ciclo privo di rischi
        self.path_to_food = computed_path_toFood #path verso la mela, da percorrere prima di usare default path

        move = graphDir_to_gameDir(self.snake.body[-1], self.path_to_food[0]) # la mossa è stata presa, aggiorniamo
        self.path_to_food.pop(0)
        self.lock.acquire()
        self.next_move = move
        self.lock.release()

        #ora inizia la parte difficile, qui possono accadere cose strane (strande inesistenti ecc...)
        while not self.termination:
            self.lock.acquire()
            calcola = True
            try:
                self.condition.wait() # soltanto per capire quando controllare se default path ancora buono
                if self.next_move != None: print('QUALCOSA DI STRANO E\' ACCADUTO') #???? non dovrebbe

                if len(self.path_to_food) > 0: #non siamo ancora arrivati alla mela
                    move = self.path_to_food.pop(0)
                    self.next_move = graphDir_to_gameDir(self.snake.body[-1], move)
                    calcola = False
                else: #abbiamo raggiunto il cibo, ora diamo una direzione safe e cerchiamo la prossima strada
                    move = self.default_path.pop(0)
                    self.next_move = graphDir_to_gameDir(self.snake.body[-1], move) # è un ciclo
                    self.default_path.append(move)

            finally: self.lock.release()

            if calcola:

                # cerchiamo una strada migliore per il cibo
                self.prec_food_position = self.food.get_positions() # TODO: si può migliorare sto schifo??
                goal = self.get_best_food()
                start = self.snake.body[-1]

                graph = Graph(self.get_true_graph(self.snake.body))
                graph.locations = self.locations
                grid_problem = GridProblem(start, goal, graph)
                search_tree = astar_search(grid_problem) #esiste il primo, per forza
                if search_tree != None: #trovato il primo
                    computed_path_toFood = search_tree.solution() #path

                    #ora calcoliamo dalla mela alla coda
                    #aggiornando il grafo con la posizione futura
                    next_pos = (self.snake.body + computed_path_toFood)[-len(self.snake.body) - 1:]
                    goal = next_pos[0] #futura coda
                    start = next_pos[-1] #futura testa

                    dummy_g = self.get_true_graph(next_pos)
                    graph = Graph(dummy_g) 
                    graph.locations = self.locations
                    grid_problem = GridProblem(start, goal, graph)
                    search_tree = astar_search(grid_problem) #esiste il primo, per forza
                    if search_tree != None: #incredibile !!! trovato anche il secondo, abbiamo finito allora
                        computed_cicle = search_tree.solution()

                        self.default_path = computed_cicle + next_pos[1:] #ciclo privo di rischi
                        self.path_to_food = computed_path_toFood #path verso la mela, da percorrere prima di usare default path

                    else: #non siamo sicuri del persorso futuro, non facciamo nulla
                        continue
                else:
                    continue #male male!! niente strada verso la mela
                
                #se siamo arrivati qui allora, abbiamo 2 percorsi
                self.lock.acquire()
                try:
                    if self.next_move != None: #abbiamo fatto in tempo !!!
                        move = self.path_to_food.pop(0)
                        self.next_move = graphDir_to_gameDir(self.snake.body[-1], move)
                        #TODO: aggiungere un meccanismo di recupero, magari aspettando un giro intero???
                    else: #siamo stati lenti, aiai
                        print('STRADA TROVATA, BOT TROPPO LENTO!!!')

                finally: self.lock.release()
    
    #TODO: creare una scelta sensata tra le mele
    def get_best_food(self):
        return self.prec_food_position[0] #una mela a caso, per ora

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
            self.next_move = None #confermare che la mossa è stata presa
            self.condition.notify(1)
        finally: self.lock.release()

        return move

    def get_true_graph(self, snake_body):
    #eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(self.grid.grid)

        for segment in snake_body[1:-1]:
            delete_cell(new_grid, segment)

        return new_grid
