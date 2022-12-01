from directions import Directions
from bot import BotS
from search import *
from grid_problem import *
import copy
import grid
import snake
import food



# ciclo ham per griglia senza ostacoli
def get_cycle(grid):
    x_blocks = grid.x_blocks
    y_blocks = grid.y_blocks

    if (x_blocks % 2) != 0 and (y_blocks % 2) != 0:
        print("Grid dimension not allowed")
        exit()

    hamcycle = {(0, 0): 0}
    value = 1

    if (x_blocks % 2) == 0:  # x_blocks PARI
        for i in range(x_blocks-1):
            i += 1
            for j in range(y_blocks-1):
                if i % 2 == 1:  # colonne dispari
                    hamcycle[(i, j)] = value
                else:
                    hamcycle[(i, y_blocks-2-j)] = value
                value += 1
        for i in range(x_blocks):
            hamcycle[(x_blocks-1-i, y_blocks-1)] = value
            value += 1
        for j in range(y_blocks-2):
            hamcycle[(0, y_blocks-2-j)] = value
            value += 1

    else:  # x_blocks DISPARI
        for i in range(y_blocks):  # i scorro le righe
            for j in range(x_blocks-1):
                if i % 2 == 0:  # righe pari
                    hamcycle[(j+1, i)] = value
                else:  # righe dispari
                    hamcycle[(x_blocks-1-j, i)] = value
                value += 1
        for i in range(y_blocks-1):
            hamcycle[(0, y_blocks-1-i)] = value
            value += 1
    return hamcycle


class Bot_hamilton(BotS):
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food: food.Food):
        self.next_move = None
        self.grid = grid
        self.snake = snake
        self.food = food

        self.ham_cycle = self.grid.get_cycle()
        # self.ham_cycle = get_cycle(self.grid)

        if len(self.snake.get_body()) < 3:
            print('LUNGHEZZA MINIMA SUPPORTATA: 3')
            exit()

        self.chosen_strat = self.hamilton_strat  # strategia

    def start(self):
        self.chosen_strat()

    def hamilton_strat(self):
        self.body = self.snake.get_body()
        self.head = self.body[-1]
        self.goal = self.food.get_positions()[0]

        grid = self.get_current_grid(self.body[:-1])
        self.grid_area = self.grid.get_grid_free_area()
        grid_problem = GridProblem(self.head, self.goal, grid, False)
        head_ham_pos = self.ham_cycle[self.head]

        for coordinates, ham_pos in self.ham_cycle.items():
            if ham_pos == (head_ham_pos + 1) % self.grid_area:
                move = (coordinates[0], coordinates[1])
                break

        if len(self.body) < 0.5 * self.grid_area:
            neighbours = grid[self.head]
            min_ham_dis = np.inf
            for next in neighbours:
                next_ham_pos = self.ham_cycle[next]
                tail_ham_pos = self.ham_cycle[self.body[0]]
                food_ham_pos = self.ham_cycle[self.goal]
                if not (self.goal == next and abs(food_ham_pos-tail_ham_pos) == 1):
                    head_rel = (head_ham_pos -
                                tail_ham_pos) % self.grid_area
                    next_rel = (next_ham_pos -
                                tail_ham_pos) % self.grid_area
                    food_rel = (food_ham_pos -
                                tail_ham_pos) % self.grid_area

                    if next_rel > head_rel and next_rel <= food_rel:
                        if food_rel - next_rel < min_ham_dis:
                            move = next

        self.next_move = self.graphDir_to_gameDir(self.head, move)
        return self.next_move

    def get_current_grid(self, snake_false_body):
        # eliminiamo dal grafo le celle occupate dal corpo dello snake
        new_grid = copy.deepcopy(self.grid.grid)

        for segment in snake_false_body:
            self.delete_cell(new_grid, segment)

        return new_grid

    def return_cycle(self):
        return self.ham_cycle

    def get_next_move(self):
        return self.chosen_strat()
