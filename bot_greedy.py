from directions import Directions
from search import *
import grid
import snake
import food
import colors
from grid_problem import *
from gui import *
import time

from bot import Bot

# debug colors
FIRST_IT_C = colors.RED
TO_FOOD_C = colors.ORANGE
DEF_C = colors.BLUE

# higher = more step before stop
DETECTLOOPGENEROSITY = 2.1
# for saving data
DECIMALDIGIT = 4
FLOATTOKEN = '%.' + str(DECIMALDIGIT) + 'f'


class Bot_greedy(Bot):

    # to create the bot
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food:food.Food, config, iterations_log, debug=False):

        # to save these variables
        super().__init__(grid, snake, food)

        # debug mode ( default=False )
        self.debug = debug

        # simple method to check if we are in a loop
        self.loop = 0
        self.max_loop = self.grid.x_blocks*self.grid.y_blocks*DETECTLOOPGENEROSITY
        
        # min lenght
        if len(self.snake.get_body()) < 3:
            print('LUNGHEZZA MINIMA SUPPORTATA: 3')
            exit() #boom

        # paths memorized
        self.default_path = []
        self.path_to_food = []
        # next node to optimize
        self.nnto = None 

        # parse the config file to save the hyperparameters
        self.parse_config(config)

        # collecting data
        self.data_to_save = []
        self.iterations_log = iterations_log
        with open(self.iterations_log, 'a+') as log:
            log.write('[\n')

    # method for parsing the cinfiguration file to memorize the hyperparameters
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

    # method for saving all the collected data of one iteration of the bot in a file
    def save_data(self):
        with open(self.iterations_log, 'a+') as log:
            line = '[\n'
            flag = True
            for a,b in self.data_to_save:
                if flag:
                    line += '\t[' + FLOATTOKEN % b + ',' + str(a) + ']'
                    flag  = False
                else:
                    line += ',[' + FLOATTOKEN % b + ',' + str(a) + ']'
            line += '],\n'
            log.write( line )
        
        self.data_to_save = []

    # method that uses the correct graph research algorithm
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
    
    # method that uses the correct optimization algorithm (only one implemented)
    def opt_search(self, start, goal, graph):
        if self.chosen_optimization == 1:
            return longest_path(graph, start, goal)
        else:
            print('Strategia ancora non implementata!!')
            exit()

    # method which is called at each failed iteration and takes care of space optimization
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
                        true_g = self.get_current_grid(to_remove)

                        #senza testa
                        #patch = get_ham_path(self.snake.fast_get_body()[-1], chokepoint, true_g)
                        patch = self.opt_search(self.snake.get_body()[-1], chokepoint, true_g)
                        if patch != None:
                            self.default_path = patch + self.default_path[choke_i + 1:]
                            self.nnto = self.default_path[choke_i + 1]
                            return #esce dal for
            
            #tg = self.get_current_grid(self.snake.fast_get_body()[-1:], tg) #solo ultima posizione
            #calcoliamo il prossimo nodo che è ottimizzabile
            for node in self.default_path[:-1]:
                if node in tg and is_optimizable(node,self.grid.grid):
                    #se lo troviamo, lo salviamo e terminiamo
                    self.nnto = node
                    #print(self.nnto)
                    return

    # returns the position of the food. Useful in cases of multiple apples               
    def get_best_food(self):
        return self.food.position

    # debug method
    def change_color(self):
        if len(self.path_to_food) > 0:
            self.snake.color = TO_FOOD_C
        else:
            self.snake.color = DEF_C

    # core of the strategy
    def apple_cicle_opt_strat(self):
        
        snake_body = self.snake.get_body()
        if self.debug: self.change_color()
        
        # if we've memorized a path to the apple, we just follow it            
        if len(self.path_to_food) > 0:
            move = self.path_to_food.pop(0)
            dir = self.snake.dir_to_cell(move)
            return dir

        # Otherwise we have to find a "path to food"
        goal = self.get_best_food()
        start = snake_body[-1]

        # we eliminate the body from the graph except the head
        dummy_g = self.get_current_grid(snake_body[:-1])
        # returns the shortest path, if it exists
        computed_path_toFood = self.graph_search(start, goal, dummy_g)

        if computed_path_toFood != None: # if it exist....
            # we calculate the position of the snake when it will eat the apple
            next_pos = (snake_body + computed_path_toFood)[-len(snake_body) - 1:]

            # we are in a cycle, so we eat the last apple before we lose
            if self.loop > self.max_loop:
                self.path_to_food = computed_path_toFood
                move = self.path_to_food.pop(0)
                self.loop = 0
                return self.snake.dir_to_cell(move)

            # if the strategy is active...
            if self.safe_cycle == 1:
                # before following the calculated route, we check if there is a safe cycle
                goal = next_pos[0] #futura tail
                start = next_pos[-1] #futura head
                dummy_g = self.get_current_grid(next_pos[1:-1]) 
                computed_cicle = self.graph_search(start, goal, dummy_g) # safe cycle

                if computed_cicle != None:
                    # if this also exists, we save the two paths and finish

                    self.default_path = computed_cicle + next_pos[1:] # safe cycle
                    self.nnto = self.default_path[1] # next optimizable cell
                    self.path_to_food = computed_path_toFood # path to food

                    move = self.path_to_food.pop(0)
                    self.loop = 0
                    return self.snake.dir_to_cell(move)
            else:
                # the strategy is not active, so we follow the path to food
                self.path_to_food = computed_path_toFood
                move = self.path_to_food.pop(0)
                self.loop = 0
                return self.snake.dir_to_cell(move)
            
        # if safe cycle is active
        if self.safe_cycle == 1:
            # we have not found a suitable path
            self.loop += 1
            self.optimize_standard_path() # we try to optimize the path we are following
            move = self.default_path.pop(0)
            ret = self.snake.dir_to_cell(move) # è un ciclo
            self.default_path.append(move)
            return ret
        else:
            
            # random move
            possible_dir = self.grid.grid[self.snake.body[-1]]
            for node in self.snake.body:
                try: possible_dir.remove(node)
                except: pass

            if len(possible_dir) > 0:
                return self.snake.dir_to_cell(possible_dir[random.randrange(len(possible_dir))])
            else:
                return Directions.random_direction()

    # the method called for the bot's next move
    def get_next_move(self):
        
        # only data collection and the call to the real strategy
        snake_body_len = len(self.snake.body)
        start_iteration_time = time.time()


        ret =  self.apple_cicle_opt_strat() 

        end_iteration_time = time.time()
        self.data_to_save.append((snake_body_len, end_iteration_time - start_iteration_time))
        
        return ret
    
    # graphic method
    def get_path_to_draw(self):
        return ([self.default_path, self.path_to_food] , [colors.YELLOW, colors.WHITE], [True, False])