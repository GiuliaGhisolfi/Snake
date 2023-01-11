from src.directions import Directions
from src.aima_search import random
import src.colors as colors
from src.grid_problem import GridProblem, astar_search_min_turns, astar_search_saving_spaces, longest_path
from src.config_parsing import read_config_file
from src.bot_player import BotPlayer

class BotGreedy(BotPlayer):
    """This class implements a bot which uses a greedy strategy to play."""

    # constant used to detect a loop 
    # (the higher it is, the more steps will be made before dying)
    LOOP_GENEROSITY = 2.1

    def __init__(
        self,
        grid,
        snake,
        food,
        config_path,
        log_path,
        test_mode,
        debug=False):

        super().__init__(grid, snake, food, config_path, log_path, test_mode)
        self.debug = debug
        self.no_improvement_counter = 0
        self.max_no_improvement = self.grid.x_blocks * self.grid.y_blocks * self.LOOP_GENEROSITY
        if len(self.snake.get_body()) < 3: # TODO: è un'assunzione necessaria?
            print('MINIMUM SUPPORTED LENGHT: 3')
            exit()
        self.default_path = []      # a long enough cycle to contain the snake's 
                                    # body but which not necessarily contains 
                                    # the food
        
        self.safe_path_to_food = [] # a safe path to the food 
                                    # (safe means that there exist a path from 
                                    # the food to the snake tail position once 
                                    # it has reached the food)
        
        self.next_opt_node = None   # first node in the default path which can
                                    # be optimized (s.t. from that node the
                                    # default path can be further extended)

    def parse_config(self, file):
        """Parse the configuration file."""
        param = read_config_file(file)
        try:
            self.chosen_search = int(param['chosen_search'])
            self.safe_cycle = int(param['safe_cycle'])
            self.chosen_optimization = int(param['chosen_optimization'])
            self.weights = []
            for s in param['weights'][1:-1].split(','):
                self.weights.append(float(s))
            self.choice_sensibility = int(param['choice_sensibility'])
        except Exception as e:
            print(e)
            print('Config values are not allowed.')
            print('Default values will be used.')
            self.chosen_search = 2
            self.safe_cycle = 1
            self.chosen_optimization = 1
            self.weights = [1, 1, 1, 1]
            self.choice_sensibility = 3

    def graph_search(self, start, goal, graph):
        """Returns a path from start to goal on graph using the chosen search 
        algorithm."""
        path_to_goal = None
        if self.chosen_search == 0:
            grid_problem = GridProblem(start, goal, graph, False)
            goal_node = astar_search_min_turns(grid_problem, self.weights)
            path_to_goal =  goal_node.solution() if goal_node != None else None
        elif self.chosen_search == 1:
            grid_problem = GridProblem(start, goal, graph, False)
            goal_node = astar_search_saving_spaces(grid_problem, self.weights)
            path_to_goal =  goal_node.solution() if goal_node != None else None
        elif self.chosen_search == 2:
            grid_problem = GridProblem(start, goal, graph, False)
            if self.choice_sensibility != 0 and \
                self.snake.length >= (self.grid.x_blocks*self.grid.y_blocks / self.choice_sensibility):
                goal_node = astar_search_saving_spaces(grid_problem, self.weights)
            else:
                goal_node = astar_search_min_turns(grid_problem, self.weights)
            path_to_goal =  goal_node.solution() if goal_node != None else None
        else: # self.chosen_search == 3
            path_to_goal = longest_path(graph, start, goal)
        
        return path_to_goal

    def optimize_default_path(self):
        """Tries to optimize the default path (extending it)."""
        if self.chosen_optimization == 0:
            return

        def get_n_neighbors(node, graph):
            """Returns the number of neighbors of node which are not in the default path."""
            count = 0
            all_neighs = graph[node]
            for neigh in all_neighs:
                if not neigh in self.default_path:
                    count += 1
            return count

        def is_optimizable(node, graph):
            """Returns true if node can be optimized 
            (has at least one neighbor which is not in the default path)."""
            return get_n_neighbors(node, graph) > 0

        def is_chokepoint(node, graph):
            """Returns true if node is a chokepoint 
            (has no neighbors which are not in the default path)."""
            return get_n_neighbors(node, graph) == 0

        # optimization is performed if the next node to optimize is the snake's head
        if self.next_opt_node != self.snake.get_body()[-1]: # TODO: che differenza c'è con riga 120? (era scritto diverso ma dovrebbe essere equivalente a come è adesso)
            return
        
        current_graph = self.grid.grid
        if is_optimizable(self.snake.get_body()[-1], current_graph):
            # find the closest chokepoint
            chokepoint = None
            for node in self.default_path[:-1]:
                if is_chokepoint(node, current_graph):
                    chokepoint = node
                    break # TODO: qui ho cambiato il codice per renderlo più leggible, è equivalente a prima giusto?
            if chokepoint == None and is_optimizable(self.snake.body[0], current_graph):
                chokepoint = self.snake.body[0]

            if chokepoint != None:
                choke_ind = self.default_path.index(chokepoint)
                # try to extend the default path as much as possible
                ctr=0 # TODO: messo per capire se fa più di una iterazione, sappiamo di casi in cui avviene?
                for node_ind in reversed(range(choke_ind + 1)):
                    ctr+=1
                    node = self.default_path[node_ind]
                    # delete from the graph the nodes which follow 'node' in the default path
                    nodes_to_del = []
                    if len(self.default_path) >= node_ind + 2:
                        nodes_to_del = self.default_path[node_ind + 1:-1]
                    new_graph = self.get_current_grid(nodes_to_del)
                    # compute the longest path to node
                    patch = longest_path(
                        grid=new_graph,
                        start=self.snake.get_body()[-1],
                        goal=node
                    )
                    # concatenate the longest path to node and the path from node to the goal
                    if patch != None:
                        self.default_path = patch + self.default_path[node_ind + 1:]
                        self.next_opt_node = self.default_path[node_ind + 1]
                        return
                if ctr > 1:
                    print("!!!!!!!!!!!")
    
        # TODO: arriva qui se la testa non può essere ottimizzata
        # oppure se può esserlo ma non sono stati trovati chokepoint e la coda non è ottimizzabile
        # oppure se un chopkepoint è stato trovato ma non è stato possibile estendere il default path
        # ma ha senso????

        # compute the next optimizable node
        # (it will be optimized when the snake reaches it)
        for node in self.default_path[:-1]:
            if node in current_graph and is_optimizable(node, self.grid.grid):
                self.next_opt_node = node
                return

    def change_color(self):
        """Changes the color of the snake for debug purposes."""
        if len(self.safe_path_to_food) > 0:
            self.snake.color = colors.ORANGE
        else:
            self.snake.color = colors.BLUE

    def strategy(self):
        snake_body = self.snake.get_body()
        if self.debug:
            self.change_color()

        # follow the safe path to the food if it has already been computed
        if len(self.safe_path_to_food) > 0:
            move = self.safe_path_to_food.pop(0)
            dir = self.snake.dir_to_cell(move)
            return dir

        # compute the path to the food
        goal = self.food.position
        start = snake_body[-1]
        current_grid = self.get_current_grid(snake_body[:-1])
        path_to_food = self.graph_search(start=start, goal=goal, graph=current_grid)

        # if a path to the food exists
        if path_to_food != None:
            # get the position of the snake's body once it has reached the food
            future_body = (snake_body + path_to_food)[-len(snake_body) - 1:]
            # in loop, follow the path to the food (and die)
            if self.no_improvement_counter > self.max_no_improvement:
                self.safe_path_to_food = path_to_food
                move = self.safe_path_to_food.pop(0)
                self.no_improvement_counter = 0
                return self.snake.dir_to_cell(move)
            # check if there is a safe cycle before following the path to the food
            if self.safe_cycle == 1:
                current_grid = self.get_current_grid(future_body[1:-1])
                path_future_head_tail = self.graph_search(
                    start=future_body[-1], # future head
                    goal=future_body[0], # future tail
                    graph=current_grid
                )
                if path_future_head_tail != None:
                    self.default_path = path_future_head_tail + future_body[1:]
                    self.next_opt_node = self.default_path[1]
                    self.safe_path_to_food = path_to_food
                    move = self.safe_path_to_food.pop(0)
                    self.no_improvement_counter = 0
                    return self.snake.dir_to_cell(move)
            else: # follow the path to the food
                self.safe_path_to_food = path_to_food
                move = self.safe_path_to_food.pop(0)
                self.no_improvement_counter = 0
                return self.snake.dir_to_cell(move)

        # a safe path does not exist
        if self.safe_cycle == 1: # try to optimize the path to the food
            self.no_improvement_counter += 1
            self.optimize_default_path()
            move = self.default_path.pop(0)
            self.default_path.append(move)
            return self.snake.dir_to_cell(move)
        else: # choose a random move
            possible_moves = self.grid.grid[self.snake.body[-1]]
            for node in self.snake.body:
                try: possible_moves.remove(node)
                except: pass
            if len(possible_moves) > 0:
                move = possible_moves[random.randrange(len(possible_moves))]
                return self.snake.dir_to_cell(move)
            else:
                return Directions.random_direction()

    def get_path_to_draw(self):
        """Returns the informations needed to draw the path on the game grid."""
        return (
            [self.default_path, self.path_to_food],
            [colors.WHITE, colors.FUXIA],
            [True, False] # TODO: in certi momenti se fermassimo la schermata i path disegnati non partono dalla testa del serpente, c'è un modo di risolvere?
                          # e poi il path fuxia non è il path verso il cibo (è una parte del vero path verso il cibo)
            )