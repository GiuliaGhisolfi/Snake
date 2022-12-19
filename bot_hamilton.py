from bot import Bot
from search import *
from grid_problem import *
import copy
import grid
import snake
import food
import colors

class Bot_hamilton(Bot):
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food: food.Food, alpha=0.5, beta=0.5):
        super().__init__(grid, snake, food)
        self.alpha = alpha
        self.beta = beta
        self.ham_cycle = self.grid.get_cycle()

        if len(self.snake.get_body()) < 3:
            print('MINIMUM LENGTH SUPPORTED: 3')
            exit()

    def set_alpha(self, alpha):
        # alpha: (snake.length / grid_area) s.t. stops greedy alg
        self.alpha = alpha
    
    def set_beta(self, beta):
        # beta: (snake.length / grid_area) s.t. stops dynamic alg
        self.beta = beta

    def get_next_move(self):
        """Hamilton strategy: the snake follows a Hamiltonian cycle generated on the 
        game grid, if possible at each iteration it tries to generate an optimal cycle 
        and/or to cut the current cycle to get as close as possible to the food position."""
        self.body = self.snake.get_body()
        self.head = self.body[-1]
        self.goal = self.food.position

        grid = self.get_current_grid(self.body[:-1])
        self.grid_area = self.grid.get_grid_free_area()

        # TODO: None?
        if self.beta != 0:  # DYNAMIC = True
            # at each iter it looks for an optimal Hamiltonian cycle for that move
            if len(self.body) < self.beta * self.grid_area:
                self.change_cycle()

        head_ham_pos = self.ham_cycle[self.head]

        for coordinates, ham_pos in self.ham_cycle.items():
            if ham_pos == (head_ham_pos + 1) % self.grid_area:
                move = coordinates # (coordinates[0], coordinates[1]) # TODO: giusto?
                break

        # TODO: None?
        if self.alpha != 0:  # GREEDY = True
            # when the snake is long we do not take shortcuts to avoid crashes
            if len(self.body) < self.alpha * self.grid_area:
                neighbors = grid[self.head]
                min_ham_dis = np.inf
                for next in neighbors:
                    next_ham_pos = self.ham_cycle[next]
                    tail_ham_pos = self.ham_cycle[self.body[0]]
                    food_ham_pos = self.ham_cycle[self.goal]
                    # if the food is adjacent to the tail we do not take shortcuts 
                    # to avoid eating the tail
                    if not (self.goal == next and abs(food_ham_pos-tail_ham_pos) == 1):
                        head_rel = (head_ham_pos - tail_ham_pos) % self.grid_area
                        next_rel = (next_ham_pos - tail_ham_pos) % self.grid_area
                        food_rel = (food_ham_pos - tail_ham_pos) % self.grid_area
                        # if next precedes the head's snake, succeds the food
                        # and is nearer to the food on the cycle, 
                        # moving there it's a shortcut
                        if next_rel > head_rel and \
                            next_rel <= food_rel and \
                            food_rel - next_rel < min_ham_dis: # TODO: giusto?
                            move = next
                            break
                            #if food_rel - next_rel < min_ham_dis:
                                #move = next
                                #break
        
        next_move = self.snake.dir_to_cell(move)
        return next_move

    def change_cycle(self):
        """Computes, if possible, a new optimal Hamiltonin cycle"""
        head_idx = self.ham_cycle[self.head]  # head value in the ham cycle
        goal_idx = self.ham_cycle[self.goal]
        tail_idx = self.ham_cycle[self.body[0]]

        # calculate position i.e. relative distance from head on ham_cycle
        goal_pos = (goal_idx - head_idx) % self.grid_area
        tail_pos = (tail_idx - head_idx) % self.grid_area

        flag = False
        if abs(goal_idx - head_idx) > 3 and goal_pos < tail_pos:
            node_neigh = self.grid.grid[self.head]
            for node in node_neigh:
                flag = False
                node_idx = self.ham_cycle[node]

                node_prec = None
                head_succ = None
                if node_idx > (head_idx + 2) and node_idx < goal_idx:
                    for nn in self.ham_cycle:
                        if self.ham_cycle[nn] == (node_idx - 1):
                            # element that has value = (node_idx - 1) on ham_cycle
                            node_prec = nn
                        if self.ham_cycle[nn] == (head_idx + 1):
                            # element that has value = (head_idx + 1) on ham cycle
                            head_succ = nn
                        if node_prec != None and head_succ != None:
                            break
                    if node_prec in self.grid.grid[head_succ]:
                        flag = True
                        node_pos = (node_idx - head_idx) % self.grid_area

                if flag:
                    flag = False
                    for n1 in self.ham_cycle:
                        for n2 in self.ham_cycle:
                            n1_idx = self.ham_cycle[n1]
                            n2_idx = self.ham_cycle[n2]
                            n1_pos = (n1_idx - head_idx) % self.grid_area
                            n2_pos = (n2_idx - head_idx) % self.grid_area
                            if n2_pos == (n1_pos + 1):
                                if n1_pos > 0 and n2_pos < node_pos:
                                    flag = True
                                    break
                        if flag:
                            break

                    if flag:
                        flag = False
                        for n1_coll in self.ham_cycle:
                            for n2_coll in self.ham_cycle:
                                n1_coll_idx = self.ham_cycle[n1_coll]
                                n2_coll_idx = self.ham_cycle[n2_coll]
                                n1_coll_pos = (
                                    n1_coll_idx - head_idx) % self.grid_area
                                n2_coll_pos = (
                                    n2_coll_idx - head_idx) % self.grid_area
                                if (n2_coll_pos > node_pos) and (n1_coll_pos == (n2_coll_pos + 1)) and \
                                        n2_coll in self.grid.grid[n2] and n1_coll in self.grid.grid[n1]:
                                    flag = True
                                    break
                            if flag:
                                break

                if flag:
                    break

        if flag:
            # change Hamiltonian cycle:
            position = np.array(list(self.ham_cycle.values()))
            # considered head in position == 0
            position = (position - head_idx) % self.grid_area 
            new_position = - np.ones((position.size,), dtype=int)

            for i in range(position.size):
                if position[i] == 0:
                    new_position[i] = 0  # head

            count = 1
            incr1 = 0
            incr2 = 1

            check = node_pos
            while check < n2_coll_pos + 1:  # nn_idx in [node, n2_coll]
                for i in range(position.size):
                    if position[i] == node_pos + count - 1:
                        new_position[i] = count
                        count += 1
                        check += 1
                        break

            check = 0
            while check < node_pos - n2_pos:  # nn_idx in [n2, node - 1]
                for i in range(position.size):
                    if position[i] == n2_pos + incr1:
                        new_position[i] = count
                        count += 1
                        incr1 += 1
                        check += 1
                        break

            check = 0
            while check < n1_pos:  # nn_idx in [head + 1, n1]
                for i in range(position.size):
                    if position[i] == incr2:
                        new_position[i] = count
                        count += 1
                        incr2 += 1
                        check += 1
                        break

            for i in range(position.size):  # nn_idx in [n1_coll, head - 1]
                if new_position[i] == -1:
                    new_position[i] = position[i]

            new_position = (new_position + head_idx) % self.grid_area
            idx = 0
            for nn in self.ham_cycle:
                self.ham_cycle[nn] = new_position[idx]
                idx += 1

    def update_ham_cycle(self):
        "Update self.ham_cycle"
        self.ham_cycle = self.grid.get_cycle()

    def get_path_to_draw(self):
        ord_list = sorted(self.ham_cycle.keys(), key=lambda k: self.ham_cycle[k])
        
        return ([ord_list] , [colors.WHITE], [True])