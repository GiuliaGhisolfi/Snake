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
from button import *

FIRST_IT_C = colors.RED
TO_FOOD_C = colors.ORANGE
DEF_C = colors.BLUE

DETECTLOOPGENEROSITY = 5

class Bot_singleplayer(BotS):
    # input anche lo snake
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food:food.Food, debug=False):

        self.grid = grid
        self.debug = debug
        #self.obstacles = obstacles

        self.snake = snake       
        self.snake.color = colors.GREEN
        self.food = food 

        self.loop = 0
        self.max_loop = self.grid.x_blocks*self.grid.y_blocks*DETECTLOOPGENEROSITY

        if len(self.snake.get_body()) < 3:
            print('LUNGHEZZA MINIMA SUPPORTATA: 3')
            exit() #boom

        self.default_path = None
        self.path_to_food = None

        #strategia attuale
        self.chosen_strat = self.mela_cicle_strat
        self.chosen_search = 2 # 0->a min turns, 1-> salva spazio, 2->mista, 3-> bonk
        self.chosen_optimization = 0 #0-> longest path

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
            dummy = longest_path(graph, start, goal)
            return dummy

        else:
            print('Strategia ancora non implementata!!')
            exit()
    
    def opt_search(self, start, goal, graph):
        if self.chosen_optimization == 0:
            return longest_path(graph, start, goal)
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
            tg = self.grid.grid

        if self.nnto == self.snake.get_body()[-1]: #next node to optimize
            #print('ping', self.nnto)
            if is_optimizable(self.snake.get_body()[-1], tg):
                #cerchiamo il prossimo choke point
                chokepoint = None
                last_n = None
                for c in self.default_path[:-1]:
                    if c in tg and is_optimizable(c, tg):
                        last_n = c
                    if c in tg and is_chokepoint(c, tg):
                        chokepoint = c
                        break
                if chokepoint == None and last_n != None:
                    chokepoint = last_n
                if chokepoint != None:
                    choke_ind = self.default_path.index(chokepoint)
                    for choke_i in reversed(range(choke_ind + 1)):
                        chokepoint = self.default_path[choke_i]

                        to_remove = []
                        if len(self.default_path) > choke_i + 2:
                            to_remove = self.default_path[choke_i + 1:-1]
                        true_g = self.get_true_graph(to_remove)

                        #senza testa
                        #patch = get_ham_path(self.snake.fast_get_body()[-1], chokepoint, true_g)
                        patch = self.opt_search(self.snake.get_body()[-1], chokepoint, true_g)
                        if patch != [] or patch != None:
                            self.default_path = patch + self.default_path[choke_i + 1:]
                            self.nnto = self.default_path[choke_i + 1]
                            return #esce dal for
            
            #tg = self.get_true_graph(self.snake.fast_get_body()[-1:], tg) #solo ultima posizione
            #calcoliamo il prossimo nodo che è ottimizzabile
            for node in self.default_path[:-1]:
                if node in tg and is_optimizable(node,self.grid.grid):
                    #se lo troviamo, lo salviamo e terminiamo
                    self.nnto = node
                    #print(self.nnto)
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
            #if self.debug:
            #    self.snake.color = FIRST_IT_C 
            
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
        #self.change_color()
        
        #ora inizia la parte difficile, qui possono accadere cose strane (strande inesistenti ecc...)       
        if len(self.path_to_food) > 0: #non siamo ancora arrivati alla mela
            move = self.path_to_food.pop(0)
            dir = self.graphDir_to_gameDir(snake_body[-1], move)
            return dir

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
                self.loop = 0
                return self.graphDir_to_gameDir(snake_body[-1], move)

        
        self.loop += 1
        self.optimize_standard_path()
        if self.loop > self.max_loop:
            return None
        move = self.default_path.pop(0)
        ret = self.graphDir_to_gameDir(snake_body[-1], move) # è un ciclo
        self.default_path.append(move)
        return ret

    def get_next_move(self):
        return self.chosen_strat()
    
