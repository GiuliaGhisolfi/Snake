import numpy as np
from src.bot import Bot
import src.gui as gui
import src.colors as colors
from src.config_parsing import read_config_file

class Bot_hamilton(Bot):
    """This class implements a bot which follows an Hamiltonian path on the grid 
    game and eventually takes shortcuts and/or tries to repair the cycle to reach 
    the food faster."""

    def __init__(self, grid, snake, food, config_path, log_path, obstacles, test_mode):
        super().__init__(grid, snake, food, config_path, log_path, test_mode)
        self.obstacles = obstacles
        if len(self.snake.get_body()) < 3:
            print('MINIMUM LENGTH SUPPORTED: 3')
            exit()
        if (grid.x_blocks % 2) != 0 and (grid.y_blocks % 2) != 0:
            gui.grid_not_allowed()

    def parse_config(self, file):
        param = read_config_file(file)
        try:
            self.max_len_shortcuts = float(param['max_len_shortcuts'])
            self.min_len_repair = float(param['min_len_repair'])
            self.max_len_repair = float(param['max_len_repair'])
        except Exception as e:
            print(e)
            print('Config values are not allowed.')
            print('Default values will be used.')
            self.max_len_shortcuts = 0.5
            self.min_len_repair = 0.45
            self.max_len_repair = 0.65

    def strategy(self):
        # restart from the same cycle at every game
        if self.restart_game:
            self.ham_cycle = self.grid.get_cycle(self.obstacles)
            self.reset_restart_game()

        self.body = self.snake.get_body()
        self.head = self.body[-1]
        self.goal = self.food.position
        grid = self.get_current_grid(self.body[:-1])
        self.grid_area = self.grid.get_grid_free_area()

        # repair the Hamiltonian cycle to reach the food faster
        if self.min_len_repair * self.grid_area < len(self.body) and \
            len(self.body) < self.max_len_repair * self.grid_area:
            self.repair_cycle()

        # get next move on the Hamiltonian cycle
        head_ham_pos = self.ham_cycle[self.head]
        for coordinates, ham_pos in self.ham_cycle.items():
            if ham_pos == (head_ham_pos + 1) % self.grid_area:
                move = coordinates
                break

        # search for shortcuts
        if len(self.body) < self.max_len_shortcuts * self.grid_area:
            neighbors = grid[self.head]
            min_dist = np.inf
            for next in neighbors:
                next_ham_pos = self.ham_cycle[next]
                tail_ham_pos = self.ham_cycle[self.body[0]]
                food_ham_pos = self.ham_cycle[self.goal]
                # if the food is adjacent to the tail, taking a shortcut could lead to a crash
                if not (self.goal == next and abs(food_ham_pos-tail_ham_pos) == 1):
                    head_rel = (head_ham_pos - tail_ham_pos) % self.grid_area
                    next_rel = (next_ham_pos - tail_ham_pos) % self.grid_area
                    food_rel = (food_ham_pos - tail_ham_pos) % self.grid_area
                    head_food_dist = food_rel - next_rel
                    if (
                        next_rel > head_rel and \
                        next_rel <= food_rel and \
                        head_food_dist < min_dist
                    ):
                        move = next
                        min_dist = head_food_dist

        next_move = self.snake.dir_to_cell(move)
        return next_move

    def repair_cycle(self):
        """Try to change the Hamiltonin cycle to reach the food faster."""
        # get head, goal and tail positions on the Hamiltonian cycle
        head_idx = self.ham_cycle[self.head]
        goal_idx = self.ham_cycle[self.goal]
        tail_idx = self.ham_cycle[self.body[0]]

        # get goal and tail relative distances w.r.t the head on the Hamiltonian cycle
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
                        for n1_adjecent in self.ham_cycle:
                            for n2_adjecnt in self.ham_cycle:
                                n1_adjecnt_idx = self.ham_cycle[n1_adjecent]
                                n2_adjecnt_idx = self.ham_cycle[n2_adjecnt]
                                n1_coll_pos = (
                                    n1_adjecnt_idx - head_idx) % self.grid_area
                                n2_adjecent_pos = (
                                    n2_adjecnt_idx - head_idx) % self.grid_area
                                if (n2_adjecent_pos > node_pos) and (n1_coll_pos == (n2_adjecent_pos + 1)) and \
                                        n2_adjecnt in self.grid.grid[n2] and n1_adjecent in self.grid.grid[n1]:
                                    flag = True
                                    break
                            if flag:
                                break

                if flag:
                    break

        if flag:
            # change the Hamiltonian cycle
            position = np.array(list(self.ham_cycle.values()))
            # consider head in position == 0
            position = (position - head_idx) % self.grid_area
            new_position = - np.ones((position.size,), dtype=int)

            for i in range(position.size):
                if position[i] == 0:
                    new_position[i] = 0  # head

            count = 1
            incr1 = 0
            incr2 = 1

            check = node_pos
            while check < n2_adjecent_pos + 1:  # nn_idx in [node, n2_adjecnt]
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

            for i in range(position.size):  # nn_idx in [n1_adjecent, head - 1]
                if new_position[i] == -1:
                    new_position[i] = position[i]

            new_position = (new_position + head_idx) % self.grid_area
            idx = 0
            for nn in self.ham_cycle:
                self.ham_cycle[nn] = new_position[idx]
                idx += 1

    def get_path_to_draw(self):
        ord_list = sorted(self.ham_cycle.keys(), key=lambda k: self.ham_cycle[k])
        return ([ord_list], [colors.WHITE], [True])