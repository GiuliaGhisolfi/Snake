import threading
from directions import Directions
from player import Player
from search import *
import copy

import grid
import snake
import food
from bot import BotS
import colors
from grid_problem import *
from bottoni import *
import longest_path as lp

FIRST_IT_C = colors.RED
TO_FOOD_C = colors.ORANGE
DEF_C = colors.BLUE


class Bot_singleplayer(BotS):
    # input anche lo snake
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food:food.Food, debug=False):

        self.grid = grid
        self.debug = debug
        #self.obstacles = obstacles

        self.snake = snake       
        self.food = food 

        if len(self.snake.get_body()) < 3:
            print('LUNGHEZZA MINIMA SUPPORTATA: 3')
            exit() #boom

        self.default_path = None
        self.path_to_food = None

        #strategia attuale
        self.chosen_strat = self.mela_cicle_strat
        self.chosen_search = 2 # 0->a min turns, 1-> salva spazio, 2->mista, 3->longest path, 4->euritica inversa
        self.chosen_optimization = 1 #0-> longest path, 1->euristica inversa

        self.nnto = None #next node to optimize


    #PER CAMBIATE LA CHIAMATA DU FUNZIONE AD A* O COSE SIMILI CAMBIARE QUESTA FUNZIONE E self.chosen_search
    def graph_search(self, start, goal, graph):
        
        if self.chosen_search == 0:
            grid_problem = GridProblem(start, goal, graph, False)
            dummy = astar_search_min_turns(grid_problem)

            if dummy != None:
                return dummy.solution()
            else: return dummy
        elif self.chosen_search == 1:
            grid_problem = GridProblem(start, goal, graph, False)
            dummy = astar_search_saving_spaces(grid_problem)

            if dummy != None:
                return dummy.solution()
            else: return dummy
        elif self.chosen_search == 2:
            grid_problem = GridProblem(start, goal, graph, False)
            dummy = astar_search_opportunistic(grid_problem, self.snake, self.grid.x_blocks*self.grid.y_blocks)

            if dummy != None:
                return dummy.solution()
            else: return dummy
        if self.chosen_search == 3:
            dummy = lp.longest_path(graph, start, goal)
            if dummy != None:
                return dummy.solution()
            else: return dummy
        if self.chosen_search == 3:
            grid_problem = GridProblem(start, goal, graph, False)
            dummy = astar_search_inverse(grid_problem)

            if dummy != None:
                return dummy.solution()
            else: return dummy

        else:
            print('Strategia ancora non implementata!!')
            exit()
    
    def opt_search(self, start, goal, graph):
        if self.chosen_optimization == 0:
            return lp.longest_path(graph, start, goal)
        elif self.chosen_optimization == 1:
            grid_problem = GridProblem(start, goal, graph, False)
            dummy = astar_search_inverse(grid_problem)

            if dummy != None:
                return dummy.solution()
            else: return dummy
        else:
            print('Strategia ancora non implementata!!')
            exit()

    #TODO: magari attuare questa strategia solo se abbastanza lunghi?
    def optimize_standard_path(self, tg={}):
        #i dizionari sono valutati false se vuoti
        
        #restituisce il numero di archi uscenti che non conducono in nodi occupati o presenti
        #in defaulth path
        def get_neighbors_n(node, true_graph):

            caselle_vicine = true_graph[node]
            tot_n = 0
            #chiavi
            for c in caselle_vicine:
                if not c in self.default_path:
                    tot_n += 1

            return tot_n
        def is_optimizable(node, true_graph):
            return get_neighbors_n(node, true_graph) > 0
        def is_chokepoint(node, true_graph):
            return get_neighbors_n(node, true_graph) == 0
        
        #definiamo tg se non già fatto
        if not tg:
            tg = self.get_true_graph(self.snake.fast_get_body()[:-1])

        if self.nnto == self.snake.fast_get_body()[-1]: #next node to optimize
            print('ping')
            if is_optimizable(self.snake.fast_get_body()[-1], tg):
                tg = self.get_true_graph([self.snake.fast_get_body()[-1]], tg)
                #cerchiamo il prossimo choke point
                chokepoint = None
                for c in self.default_path[:-1]:
                    if c in tg and is_chokepoint(c, tg):
                        chokepoint = c
                        break
                if chokepoint != None:
                    choke_ind = self.default_path.index(chokepoint)
                    for choke_i in reversed(range(choke_ind + 1)):
                        chokepoint = self.default_path[choke_i]

                        to_remove = []
                        if len(self.default_path) > choke_i + 2:
                            to_remove = self.default_path[choke_i + 1:-1]
                        true_g = self.get_true_graph(self.snake.fast_get_body()[:-1] + to_remove)

                        #senza testa
                        #patch = get_ham_path(self.snake.fast_get_body()[-1], chokepoint, true_g)
                        patch = lp.longest_path(true_g, self.snake.fast_get_body()[-1], chokepoint)
                        if patch != None:
                            self.default_path = patch + self.default_path[choke_i + 1:]

                            print('Ottimizzato', chokepoint)
                            self.nnto = self.default_path[len(patch)]
                            return #esce dal for
            else:
                tg = self.get_true_graph(self.snake.fast_get_body()[-1:], tg) #solo ultima posizione
                #calcoliamo il prossimo nodo che è ottimizzabile
                for node in self.default_path[:-1]:
                    if node in tg and is_optimizable(node,tg):
                        #se lo troviamo, lo salviamo e terminiamo
                        self.nnto = node
                        print(self.nnto)
                        return
                        
    def get_best_food(self):
        return self.food.get_positions()[0] #una mela a caso, per ora
    
    def get_true_graph(self, snake_false_body, grid={}):
        if not grid:
            grid = self.grid.grid # da controllare

        #eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(grid) #forse ci va messo grid?

        for segment in snake_false_body: #manca la testa
            self.delete_cell(new_grid, segment)

        return new_grid

    def change_color(self):
        if self.debug:
            if len(self.path_to_food) > 0:
                self.snake.color = TO_FOOD_C
            else:
                self.snake.color = DEF_C

    # funzione usata per chiedere la prossima mossa dello snake
    def mela_cicle_strat(self):

        # inizio e basta
        if self.default_path == None and self.path_to_food == None:
            if self.debug:
                self.snake.color = FIRST_IT_C 
            
            snake_body = self.snake.get_body()

            # posizione mela migliore e testa snake
            goal = self.get_best_food()
            start = snake_body[-1]

            #elimino tutto il corpo tranne la testa del serpente dal grafo
            dummy_g = self.get_true_graph(snake_body[:-1])
            computed_path_toFood = self.graph_search(start, goal, dummy_g)
        
            #aggiornando il grafo con la posizione futura
            next_pos = (snake_body + computed_path_toFood)[-len(snake_body) - 1:]
            goal = next_pos[0] #futura coda
            start = next_pos[-1] #futura testa

            #ora calcoliamo dalla mela (mangiata) alla coda, elimino coda e testa dello snake
            dummy_g = self.get_true_graph(next_pos[1:-1])
            computed_cicle = self.graph_search(start, goal, dummy_g)

            self.default_path = computed_cicle + next_pos[1:] #ciclo privo di rischi
            self.nnto = self.default_path[1]
            self.path_to_food = computed_path_toFood #path verso la mela, da percorrere prima di usare default path
            
            #la mossa è stata presa, aggiorniamo
            #calcolo direzione verso la mela
            c = self.path_to_food.pop(0)
            return self.graphDir_to_gameDir(snake_body[-1], c) 

        snake_body = self.snake.get_body()
        self.change_color()
        
        #ora inizia la parte difficile, qui possono accadere cose strane (strande inesistenti ecc...)       
        if len(self.path_to_food) > 0: #non siamo ancora arrivati alla mela
            move = self.path_to_food.pop(0)
            return self.graphDir_to_gameDir(snake_body[-1], move)

 
        # posizione mela migliore e testa snake
        goal = self.get_best_food()
        start = snake_body[-1]

        #elimino tutto il corpo tranne la testa del serpente dal grafo
        dummy_g = self.get_true_graph(snake_body[:-1])
        #restituisce il cammino se esiste, più pulito di prima
        computed_path_toFood = self.graph_search(start, goal, dummy_g)

        if computed_path_toFood != None: #trovato il primo
            #uguale a prima con una accortezza di differenza
            next_pos = (snake_body + computed_path_toFood)[-len(snake_body) - 1:]
            goal = next_pos[0] #futura coda
            start = next_pos[-1] #futura testa
            dummy_g = self.get_true_graph(next_pos[1:-1]) #non eliminiamo la coda
            computed_cicle = self.graph_search(start, goal, dummy_g)

            if computed_cicle != None: #incredibile !!! trovato anche il secondo, abbiamo finito allora
                self.default_path = computed_cicle + next_pos[1:] #ciclo privo di rischi
                self.nnto = self.default_path[1]
                self.path_to_food = computed_path_toFood #path verso la mela, da percorrere prima di usare default path

                move = self.path_to_food.pop(0)
                return self.graphDir_to_gameDir(snake_body[-1], move)

        self.optimize_standard_path()
        move = self.default_path.pop(0)
        ret = self.graphDir_to_gameDir(snake_body[-1], move) # è un ciclo
        self.default_path.append(move)
        return ret

    def get_next_move(self):
        return self.chosen_strat()
    
