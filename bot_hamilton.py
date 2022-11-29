from directions import Directions
from bot import BotS
from search import *
from grid_problem import *
import copy
import grid
import snake
import food

# Se False utilizza a*, altrimenti cerca di fare tagli in tutte le celle vicine 
# alla testa e sceglie quella più vicina alla mela sul ciclo hamiltoniano
GREEDY = True

# ciclo ham per griglia senza ostacoli
def get_cycle(grid):
    x_blocks = grid.x_blocks
    y_blocks = grid.y_blocks
    
    # TODO: spostare check
    if (x_blocks % 2) != 0 and (y_blocks % 2) != 0:
        print("Grid dimension not allowed")
        exit()
    
    hamcycle = {(0,0): 0}
    value = 1
    
    if (x_blocks % 2) == 0: # x_blocks PARI
        for i in range(x_blocks-1):
            i += 1
            for j in range(y_blocks-1):
                if i % 2 == 1: # colonne dispari
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

    else: # x_blocks DISPARI   
        for i in range(y_blocks): #i scorro le righe            
            for j in range(x_blocks-1):
                if i % 2 == 0: # righe pari
                    hamcycle[(j+1, i)] = value
                else: # righe dispari       
                    hamcycle[(x_blocks-1-j, i)] = value
                value += 1
        for i in range(y_blocks-1):
            hamcycle[(0, y_blocks-1-i)] = value
            value += 1
    return hamcycle

def cycle8():
    # ciclo hamiltoniano per matrix 8x8 molto a zig zag
    # TODO: togliere o implementare in modo parametrico
    hamcycle = {(0, 0): 0, (0, 1): 1, (0, 2): 4, (0, 3): 5, (0, 4): 8, (0, 5): 9, (0, 6): 12, (0, 7): 13, 
        (1, 0): 63, (1, 1): 2, (1, 2): 3, (1, 3): 6, (1, 4): 7, (1, 5): 10, (1, 6): 11, (1, 7): 14, 
        (2, 0): 62, (2, 1): 27, (2, 2): 26, (2, 3): 23, (2, 4): 22, (2, 5): 19, (2, 6): 18, (2, 7): 15, 
        (3, 0): 61, (3, 1): 28, (3, 2): 25, (3, 3): 24, (3, 4): 21, (3, 5): 20, (3, 6): 17, (3, 7): 16, 
        (4, 0): 60, (4, 1): 29, (4, 2): 32, (4, 3): 33, (4, 4): 36, (4, 5): 37, (4, 6): 40, (4, 7): 41, 
        (5, 0): 59, (5, 1): 30, (5, 2): 31, (5, 3): 34, (5, 4): 35, (5, 5): 38, (5, 6): 39, (5, 7): 42, 
        (6, 0): 58, (6, 1): 55, (6, 2): 54, (6, 3): 51, (6, 4): 50, (6, 5): 47, (6, 6): 46, (6, 7): 43, 
        (7, 0): 57, (7, 1): 56, (7, 2): 53, (7, 3): 52, (7, 4): 49, (7, 5): 48, (7, 6): 45, (7, 7): 44}
    return hamcycle

class Bot_hamilton(BotS):
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food: food.Food):
        self.next_move = None
        self.grid = grid
        self.snake = snake
        self.food = food
        self.ham_cycle = self.grid.get_cycle()

        # TODO: spostare check
        if len(self.snake.get_body()) < 3:
            print('LUNGHEZZA MINIMA SUPPORTATA: 3')
            exit()
              
        self.chosen_strat = self.hamilton_cicle_start # strategia

    def start(self):
        self.chosen_strat()
    
    def snake_in_hamilton(self, ham_cycle):
        # TODO: trovare un modo intelligente per invertire per correnza di ham, altrimenti togliere
        prec_node = self.snake.body[0]
        prec_value = ham_cycle[prec_node] # value of the node in hamilton cycle
        grid_area = self.grid.x_blocks * self.grid.y_blocks
        flag = 1 # default True
        for node in self.snake.body[1:] :
            value = ham_cycle[node]
            if (value != prec_value + 1) and not (value == 0 and prec_value == (grid_area - 1) ):
                flag = 0
            prec_value = value
        # flag = 1 sono tutta dentro ad ham -> posso girarmi
        return flag

    def hamilton_cicle_start(self):
        body = self.snake.get_body()
        head = body[-1]
        goal = self.food.get_positions()[0]

        grid = self.get_current_grid(body[:-1])
        grid_area = self.grid.get_grid_free_area()
        grid_problem = GridProblem(head, goal, grid, False)

        head_ham_pos = self.ham_cycle[head]

        for coordinates, ham_pos in self.ham_cycle.items():
            if ham_pos == (head_ham_pos + 1) % grid_area:
                move = (coordinates[0], coordinates[1])
                break

        if len(body) < 0.5 * grid_area:
            if GREEDY:
                neighbours = grid[head]
                min_ham_dis = np.inf
                for next in neighbours:
                    next_ham_pos = self.ham_cycle[next]
                    tail_ham_pos = self.ham_cycle[body[0]]
                    food_ham_pos = self.ham_cycle[goal]
                    if not (goal == next and abs(food_ham_pos-tail_ham_pos) == 1):
                        head_rel = (head_ham_pos - tail_ham_pos) % grid_area
                        next_rel = (next_ham_pos - tail_ham_pos) % grid_area
                        food_rel = (food_ham_pos - tail_ham_pos) % grid_area
                        if next_rel > head_rel and next_rel <= food_rel:
                            if food_rel - next_rel < min_ham_dis:
                                move = next
            else:
                goal_node = astar_search(grid_problem)
                if goal_node != None:
                    # cerco di seguire il path di a*, se riesco a farlo ritornando sul ciclo ham
                    path = goal_node.solution()
                    next_ham_pos = self.ham_cycle[path[0]] # netx idx (seguendo path a*)
                    tail_ham_pos = self.ham_cycle[body[0]]
                    food_ham_pos = self.ham_cycle[goal]
                    if not (len(path) == 1 and abs(food_ham_pos-tail_ham_pos) == 1):
                        head_rel = (head_ham_pos - tail_ham_pos) % grid_area
                        # distanza tra tail e head, seguendo ciclo ham ( == len(snake.body) solo se è tutto sul ciclo)
                        next_rel = (next_ham_pos - tail_ham_pos) % grid_area
                        # distanza tra tail e prossima cella occupata dal path a*, seguendo ciclo ham
                        food_rel = (food_ham_pos - tail_ham_pos) % grid_area
                        # distanza tra tail e food position, seguendo ciclo ham
                        if next_rel > head_rel and next_rel <= food_rel:
                            # dist da tail snake a cella a* > len snake (i.e. non mi mangio) and
                            # dist da tail snake a cella a* <= dist food a tail (i.e. faccio un taglio utile e non supero la mela)
                            move = path[0] # seguo path a*
                        
        # TODO: check che mi posso mettere dentro al contrario
        # riscrivere tutte le funzioni per leggere dizionario da (grid_area-1) a 0
        # MA HA SENSO???
        # se riusciamo a fare i tagli bene è meglio!!!!!!!!!!
        # anche partendo dai cicli ham più semplici
        self.next_move = self.graphDir_to_gameDir(head, move)
        return self.next_move

    def get_current_grid(self, snake_false_body):
        # eliminiamo dal grafo le celle occupate dal corpo dello snake
        new_grid = copy.deepcopy(self.grid.grid)

        for segment in snake_false_body:
            self.delete_cell(new_grid, segment)

        return new_grid
    
    def get_next_move(self):
        return self.chosen_strat()
    
    def update_ham_cycle(self):
        self.ham_cycle = self.grid.get_cycle()
