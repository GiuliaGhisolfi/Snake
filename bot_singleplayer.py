from directions import Directions
from player import Player
from search import *
import copy
import grid
import snake
import food
import colors
from grid_problem import *
from button import *
import time

from bot import Bot

FIRST_IT_C = colors.RED
TO_FOOD_C = colors.ORANGE
DEF_C = colors.BLUE

# higher = more step before stop
DETECTLOOPGENEROSITY = 2.1
DECIMALDIGIT = 4
FLOATTOKEN = '%.' + str(DECIMALDIGIT) + 'f'

# IRENE: sarebbe possibile sostituire le invocazoni di self.graphDir_to_gameDir() con 
# dir_to_cell(), metodo della classe Snake?
# Così possiamo eliminare del tutto il metodo graphDir_to_gameDir che ha poco a che fare con la classe Bot...
# ma certo! bella idea

class Bot_singleplayer(Bot):

    # to create the bot
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food:food.Food, debug=False, config='singleplayer.config', logname='singleplayer_log.csv', info=''):

        # the grid with the obstacles
        self.grid = grid
        # debug variable ( default=False )
        self.debug = debug

        self.snake = snake       
        self.food = food 

        # simple method to check if we are in a loop
        self.loop = 0
        self.max_loop = self.grid.x_blocks*self.grid.y_blocks*DETECTLOOPGENEROSITY

        if len(self.snake.get_body()) < 3:
            print('LUNGHEZZA MINIMA SUPPORTATA: 3')
            exit() #boom

        # paths memorized
        self.default_path = []
        self.path_to_food = []
        # next node to optimize
        self.nnto = None 

        self.parse_config(config)
 
        
        bot_type = 'singleplayer_bot [' + str(self.chosen_search) + '|' + str(self.safe_cycle)  +  '|' + str(self.chosen_optimization) + '|' + str(self.weights) + '|' + str(self.choice_sensibility) + ']' + info

        self.data_to_save = [bot_type, 0, False, 0, []]
        self.logname = logname
        
        self.total_bot_time = 0
        self.total_iteration = 0

    def parse_config(self, file):
        param = {}
        with open(file, 'r') as c:
            for i, line in enumerate(c):
                if line.startswith('#') or len(line) == 1:
                    continue
                else:
                    try:
                        sl = line.replace('\n', '').replace(' ', '').split('=')
                        param[sl[0]] = sl[1]
                    except:
                        print('errore file config linea: '  + str(i))

        try:
            self.chosen_search = int(param['chosen_search'])
            # safe path strategy
            # 0 -> no, 1 -> yes
            self.safe_cycle = int(param['safe_cycle'])
            # space optimization search
            # 0 -> nothing, 1-> longest path
            self.chosen_optimization = int(param['chosen_optimization'])

            self.weights = [] #weight for the A* heuristic
            for s in param['weights'][1:-1].split(','):
                self.weights.append(float(s))
            self.choice_sensibility = int(param['choice_sensibility'])

        except Exception as e:
            print(e)
            print('parameter value error')
            print('initialization with default values')

            self.chosen_search = 2 
            self.safe_cycle = 1
            self.chosen_optimization = 1
            self.weights = [1,0,0,0]
            self.choice_sensibility = 4

    def save_data(self, result):

        self.data_to_save[1] = self.total_bot_time
        self.data_to_save[2] = result
        self.data_to_save[3] = self.total_iteration

        with open(self.logname, 'a+') as log:
            line = self.data_to_save[0]
            line += ','

            line += FLOATTOKEN % self.data_to_save[1]
            line += ','

            line += str(self.data_to_save[2])
            line += ','

            line += FLOATTOKEN % self.data_to_save[3]
            line += ','

            line += '['
            first = True
            for a,b in self.data_to_save[4]:
                if first:
                    first = False
                    line += '(' + FLOATTOKEN % a + ',' + str(b) + ')'
                else:
                    line += ',(' + FLOATTOKEN % a + ',' + str(b) + ')'
            line += ']\n'

            log.write( line )

        self.total_iteration = 0
        self.total_bot_time = 0

    #PER CAMBIATE LA CHIAMATA DU FUNZIONE AD A* O COSE SIMILI CAMBIARE QUESTA FUNZIONE E self.chosen_search
    def graph_search(self, start, goal, graph):
        
        if self.chosen_search == 0:
            grid_problem = GridProblem(start, goal, graph, False)
            dummy = astar_search_min_turns(grid_problem, self.weights)

            if dummy != None:
                return dummy.solution()
            else: return dummy
        elif self.chosen_search == 1:
            grid_problem = GridProblem(start, goal, graph, False)
            dummy = astar_search_saving_spaces(grid_problem, self.weights)

            if dummy != None:
                return dummy.solution()
            else: return dummy
        elif self.chosen_search == 2:
            grid_problem = GridProblem(start, goal, graph, False)
            if self.snake.length >= (self.grid.x_blocks*self.grid.y_blocks /self.choice_sensibility):
                dummy = astar_search_saving_spaces(grid_problem, self.weights)
            else:
                dummy = astar_search_min_turns(grid_problem, self.weights)

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
        if self.chosen_optimization == 1:
            return longest_path(graph, start, goal)
        else:
            print('Strategia ancora non implementata!!')
            exit()

    #TODO: magari attuare questa strategia solo se abbastanza lunghi?
    def optimize_standard_path(self, tg={}):
        # no space optimization
        if self.chosen_optimization == 0: return
        
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
                        if patch != None:
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
        return self.food.position
    
    # IRENE: siccome è uguale al metodo get_current_grid in bot_hamilton,
    #  se lo spostassimo nella classe bot facendo un costruttore con gli 
    # attributi comuni a entrambi da invocare nel costruttore delle sotto classi?

    # facciamo! 
    def get_true_graph(self, snake_false_body): # IRENE: possiamo togliere il parametro grid? (non viene mai passato)
        
        grid = self.grid
        #eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(grid)

        for segment in snake_false_body: #manca la testa

            new_grid.delete_cell(segment)

        return new_grid.grid

    def change_color(self):
        if len(self.path_to_food) > 0:
            self.snake.color = TO_FOOD_C
        else:
            self.snake.color = DEF_C

    # funzione usata per chiedere la prossima mossa dello snake
    def apple_cicle_opt_strat(self):
            
        
        snake_body = self.snake.get_body()
        if self.debug: self.change_color()
        
        #ora inizia la parte difficile, qui possono accadere cose strane (strande inesistenti ecc...)       
        if len(self.path_to_food) > 0: #non siamo ancora arrivati alla mela
            move = self.path_to_food.pop(0)
            dir = self.snake.dir_to_cell(move)
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

            # we are in a cycle, so we eat the last apple before we lose
            if self.loop > self.max_loop:
                self.path_to_food = computed_path_toFood
                move = self.path_to_food.pop(0)
                self.loop = 0
                return self.snake.dir_to_cell(move)

            if self.safe_cycle == 1:
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
                    return self.snake.dir_to_cell(move)
            else:
                self.path_to_food = computed_path_toFood
                move = self.path_to_food.pop(0)
                self.loop = 0
                return self.snake.dir_to_cell(move)
            

        if self.safe_cycle == 1:
            self.loop += 1
            self.optimize_standard_path()
            move = self.default_path.pop(0)
            ret = self.snake.dir_to_cell(move) # è un ciclo
            self.default_path.append(move)
            return ret
        else:
            possible_dir = self.grid.grid[self.snake.body[-1]]
            if len(possible_dir) > 0:
                return self.snake.dir_to_cell(possible_dir[0])
            else:
                return Directions.random_direction()

    def get_next_move(self):
      
        snake_body_len = len(self.snake.body)
        start_iteration_time = time.time()

        self.total_iteration += 1

        ret =  self.apple_cicle_opt_strat() 

        end_iteration_time = time.time()
        self.data_to_save[4].append((end_iteration_time - start_iteration_time, snake_body_len))

        self.total_bot_time += end_iteration_time - start_iteration_time
        return ret
        # IRENE: se qui invocassimo direttamente la strategia visto che ne abbiamo implementata una sola?
        # ciò renderebbe il codice più uniforme a bot_hamilton
        # 
        # GIACOMO si ma non solo...
        # Invincibile, Impavido, 
        # Sensuale, Misterioso, 
        # Ammaliante, Vigoroso, 
        # Diligente, Travolgente, 
        # Stupendo, Passionale, 
        # Terrificante, Bello, 
        # Forte Bianco Principe GECO:
        # oora è utile per i dati, magari conviene farlo anche in ham?
    
