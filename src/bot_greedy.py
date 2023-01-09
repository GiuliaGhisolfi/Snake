from src.directions import Directions
from src.aima_search import random
import src.colors as colors
from src.grid_problem import GridProblem, astar_search_min_turns, astar_search_saving_spaces, longest_path
from src.config_parsing import read_config_file
from src.bot import Bot

class Bot_greedy(Bot):
    """This class implements a bot which uses a greedy strategy to play."""

    # the higher it is, the more steps will be made before dying
    LOOP_GENEROSITY = 2.1

    def __init__(self, grid, snake, food, config_path, log_path, test_mode, debug=False):
        super().__init__(grid, snake, food, config_path, log_path, test_mode)
        self.debug = debug
        self.loop = 0
        self.max_loop = self.grid.x_blocks * self.grid.y_blocks * self.LOOP_GENEROSITY
        if len(self.snake.get_body()) < 3:
            print('MINIMUM SUPPORTED LENGHT: 3')
            exit()
        self.default_path = []
        self.path_to_food = []
        self.next_opt_node = None

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
            self.chosen_optimization = 1 # TODO: change with best
            self.weights = [1, 0, 0, 0]
            self.choice_sensibility = 4

    def graph_search(self, start, goal, graph):
        """Returns a path from start to goal on graph using chosen_search."""
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
        elif self.chosen_search == 3:
            path_to_goal = longest_path(graph, start, goal)
        
        return path_to_goal

    def optimize_standard_path(self):
        """Tries to optimize the space occupied by the snake on the grid."""
        if self.chosen_optimization == 0:
            return

        def get_n_neighbors(node, true_graph):
            """Returns the number of neighboring nodes which are not in the default path."""
            count = 0
            all_neighs = true_graph[node]
            for neigh in all_neighs:
                if not neigh in self.default_path:
                    count += 1
            return count

        def is_optimizable(node, true_graph):
            """Returns true if the node can be optimized."""
            return get_n_neighbors(node, true_graph) > 0

        def is_chokepoint(node, true_graph):
            """Returns true if the node is a chokepoint."""
            return get_n_neighbors(node, true_graph) == 0

        true_graph = self.grid.grid
        if self.next_opt_node == self.snake.get_body()[-1]:
            if is_optimizable(self.snake.get_body()[-1], true_graph):
                # find the closest chokepoint
                chokepoint = None
                last_n = None
                for node in self.default_path[:-1]:
                    if is_chokepoint(node, true_graph):
                        chokepoint = node
                        break
                    if node == self.snake.body[0] and is_optimizable(node, true_graph):
                        last_n = node
                        break
                if chokepoint == None and last_n != None:
                    chokepoint = last_n
                # TODO: if chokepoint == None and is_optimizable(self.snake.body[0], true_graph):
                #   chokepoint = self.snake.body[0]

                if chokepoint != None:
                    choke_ind = self.default_path.index(chokepoint)
                    for choke_i in reversed(range(choke_ind + 1)):
                        chokepoint = self.default_path[choke_i]

                        nodes_to_del = []
                        if len(self.default_path) >= choke_i + 2:
                            nodes_to_del = self.default_path[choke_i + 1:-1]
                        true_g = self.get_current_grid(nodes_to_del)

                        patch = longest_path(
                            grid=true_g,
                            start=self.snake.get_body()[-1],
                            goal=chokepoint
                        )

                        if patch != None:
                            self.default_path = patch + self.default_path[choke_i + 1:]
                            self.next_opt_node = self.default_path[choke_i + 1]
                            return

            # compute the next optimizable node
            for node in self.default_path[:-1]:
                if node in true_graph and is_optimizable(node, self.grid.grid):
                    self.next_opt_node = node
                    return

    def change_color(self):
        """Changes the color of the snake for debug purposes."""
        if len(self.path_to_food) > 0:
            self.snake.color = colors.ORANGE
        else:
            self.snake.color = colors.BLUE

    def strategy(self):
        snake_body = self.snake.get_body()
        if self.debug:
            self.change_color()

        # follow the path to the food it has already been computed
        if len(self.path_to_food) > 0:
            move = self.path_to_food.pop(0)
            dir = self.snake.dir_to_cell(move)
            return dir

        goal = self.food.position
        start = snake_body[-1]
        current_grid = self.get_current_grid(snake_body[:-1])
        path_to_food = self.graph_search(start=start, goal=goal, graph=current_grid)

        if path_to_food != None:
            # compute the position of the snake when it eats the food
            next_pos = (snake_body + path_to_food)[-len(snake_body) - 1:]

            # in loop, eat the last food (and die)
            if self.loop > self.max_loop:
                self.path_to_food = path_to_food
                move = self.path_to_food.pop(0)
                self.loop = 0
                return self.snake.dir_to_cell(move)

            # check if there is a safe cycle before following the path to the food
            if self.safe_cycle == 1:
                current_grid = self.get_current_grid(next_pos[1:-1])
                cycle = self.graph_search(
                    start=next_pos[-1],
                    goal=next_pos[0],
                    graph=current_grid
                )
                if cycle != None:
                    self.default_path = cycle + next_pos[1:]
                    self.next_opt_node = self.default_path[1]
                    self.path_to_food = path_to_food
                    move = self.path_to_food.pop(0)
                    self.loop = 0
                    return self.snake.dir_to_cell(move)
            else: # follow the path to food
                self.path_to_food = path_to_food
                move = self.path_to_food.pop(0)
                self.loop = 0
                return self.snake.dir_to_cell(move)

        # a safe cycle does not exist
        if self.safe_cycle == 1: # try to optimize the path
            self.loop += 1
            self.optimize_standard_path()
            move = self.default_path.pop(0)
            ret = self.snake.dir_to_cell(move)
            self.default_path.append(move)
            return ret
        else: # choose a random move
            possible_dir = self.grid.grid[self.snake.body[-1]]
            for node in self.snake.body:
                try: possible_dir.remove(node)
                except: pass
            if len(possible_dir) > 0:
                move = possible_dir[random.randrange(len(possible_dir))]
                return self.snake.dir_to_cell(move)
            else:
                return Directions.random_direction()

    def get_path_to_draw(self):
        """Returns the informations needed to draw the path on the game grid."""
        return (
            [self.default_path, self.path_to_food],
            [colors.YELLOW, colors.WHITE],
            [True, False]
            )