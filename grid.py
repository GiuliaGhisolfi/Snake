import copy
import random as rand

class Grid:
    def __init__(self, size, x_blocks, y_blocks):
        self.size = size
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        x_pixel = size-(size % x_blocks)
        self.bounds = (x_pixel, x_pixel*y_blocks/x_blocks)
        self.block_size = x_pixel/x_blocks
        self.full_grid = self.build_grid()
        self.grid = copy.deepcopy(self.full_grid)
        self.obstacles = []

        # MAPPE DEL GIOCO:
        self.configs = [
            [
                (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12),
                (3, 7), (4, 7), (5, 7), (6, 7), (8, 7), (9, 7), (10, 7), (11, 7)
            ], #ostacolo +
            [
                (5, 0), (6, 0), (7, 0),
                (4, 3), (4, 4), (4, 5),
                (12, 2), (12, 3), (12, 4),
                (8, 6), (8, 7), (9, 6), (9, 7),
                (9, 10), (10, 10), (11, 10), (12, 10),
                (3, 11), (4, 11), (5, 11), (3, 12), (4, 12), (5, 12), (3, 13), (4, 13), (5, 13),
            ], #ostacoli a blocchi e a pareti
            [
                (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4),
                (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8),
                (4, 11), (5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11), (11, 11), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (11, 12)
            ], #ostacoli tunnel
            [
                (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
                (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4),
                (0, 11), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11),
                (9, 10), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15)
            ] #spirale
        ]

        self.hamcycles = [
            {
                (0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (0, 4): 16, (0, 5): 17, (0, 6): 30, (0, 7): 31, (0, 8): 32, (0, 9): 33, (0, 10): 34, (0, 11): 35, (0, 12): 36, (0, 13): 37, (0, 14): 38, (0, 15): 39,
                (1, 0): 221, (1, 1): 194, (1, 2): 193, (1, 3): 4, (1, 4): 15, (1, 5): 18, (1, 6): 29, (1, 7): 48, (1, 8): 47, (1, 9): 46, (1, 10): 45, (1, 11): 44, (1, 12): 43, (1, 13): 42, (1, 14): 41, (1, 15): 40,
                (2, 0): 220, (2, 1): 195, (2, 2): 192, (2, 3): 5, (2, 4): 14, (2, 5): 19, (2, 6): 28, (2, 7): 49, (2, 8): 50, (2, 9): 51, (2, 10): 52, (2, 11): 53, (2, 12): 54, (2, 13): 55, (2, 14): 56, (2, 15): 57,
                (3, 0): 219, (3, 1): 196, (3, 2): 191, (3, 3): 6, (3, 4): 13, (3, 5): 20, (3, 6): 27, (3, 8): 65, (3, 9): 64, (3, 10): 63, (3, 11): 62, (3, 12): 61, (3, 13): 60, (3, 14): 59, (3, 15): 58,
                (4, 0): 218, (4, 1): 197, (4, 2): 190, (4, 3): 7, (4, 4): 12, (4, 5): 21, (4, 6): 26, (4, 8): 66, (4, 9): 67, (4, 10): 68, (4, 11): 69, (4, 12): 70, (4, 13): 71, (4, 14): 72, (4, 15): 73,
                (5, 0): 217, (5, 1): 198, (5, 2): 189, (5, 3): 8, (5, 4): 11, (5, 5): 22, (5, 6): 25, (5, 8): 81, (5, 9): 80, (5, 10): 79, (5, 11): 78, (5, 12): 77, (5, 13): 76, (5, 14): 75, (5, 15): 74,
                (6, 0): 216, (6, 1): 199, (6, 2): 188, (6, 3): 9, (6, 4): 10, (6, 5): 23, (6, 6): 24, (6, 8): 82, (6, 9): 83, (6, 10): 84, (6, 11): 85, (6, 12): 86, (6, 13): 87, (6, 14): 90, (6, 15): 91,
                (7, 0): 215, (7, 1): 200, (7, 2): 187, (7, 13): 88, (7, 14): 89, (7, 15): 92,
                (8, 0): 214, (8, 1): 201, (8, 2): 186, (8, 3): 173, (8, 4): 172, (8, 5): 159, (8, 6): 158, (8, 8): 100, (8, 9): 99, (8, 10): 98, (8, 11): 97, (8, 12): 96, (8, 13): 95, (8, 14): 94, (8, 15): 93,
                (9, 0): 213, (9, 1): 202, (9, 2): 185, (9, 3): 174, (9, 4): 171, (9, 5): 160, (9, 6): 157, (9, 8): 101, (9, 9): 102, (9, 10): 103, (9, 11): 104, (9, 12): 105, (9, 13): 106, (9, 14): 107, (9, 15): 108,
                (10, 0): 212, (10, 1): 203, (10, 2): 184, (10, 3): 175, (10, 4): 170, (10, 5): 161, (10, 6): 156, (10, 8): 116, (10, 9): 115, (10, 10): 114, (10, 11): 113, (10, 12): 112, (10, 13): 111, (10, 14): 110, (10, 15): 109,
                (11, 0): 211, (11, 1): 204, (11, 2): 183, (11, 3): 176, (11, 4): 169, (11, 5): 162, (11, 6): 155, (11, 8): 117, (11, 9): 118, (11, 10): 119, (11, 11): 120, (11, 12): 121, (11, 13): 122, (11, 14): 123, (11, 15): 124,
                (12, 0): 210, (12, 1): 205, (12, 2): 182, (12, 3): 177, (12, 4): 168, (12, 5): 163, (12, 6): 154, (12, 7): 153, (12, 8): 132, (12, 9): 131, (12, 10): 130, (12, 11): 129, (12, 12): 128, (12, 13): 127, (12, 14): 126, (12, 15): 125,
                (13, 0): 209, (13, 1): 206, (13, 2): 181, (13, 3): 178, (13, 4): 167, (13, 5): 164, (13, 6): 151, (13, 7): 152, (13, 8): 133, (13, 9): 134, (13, 10): 135, (13, 11): 136, (13, 12): 137, (13, 13): 138, (13, 14): 139, (13, 15): 140,
                (14, 0): 208, (14, 1): 207, (14, 2): 180, (14, 3): 179, (14, 4): 166, (14, 5): 165, (14, 6): 150, (14, 7): 149, (14, 8): 148, (14, 9): 147, (14, 10): 146, (14, 11): 145, (14, 12): 144, (14, 13): 143, (14, 14): 142, (14, 15): 141
            }
        ]

    def build_grid(self):
        def neighbors(x, y):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for (dx, dy) in directions:
                (nx, ny) = (x + dx, y + dy)
                if  0 <= nx < self.x_blocks and 0 <= ny < self.y_blocks:
                    yield (nx, ny)
        
        grid = {}
        for x in range(self.x_blocks):
            for y in range(self.y_blocks):
                grid[(x, y)] = list(neighbors(x, y))
        return grid


    def draw_obstacles(self, game, window):
        for i in range(len(self.obstacles)):
            game.draw.rect(
                window,
                self.obstacles[i].color,
                ((self.obstacles[i].x_position) * self.block_size +1 , (self.obstacles[i].y_position) * self.block_size +1, self.block_size-2, self.block_size-2))

    
    def spawn_obstacles(self):
        self.grid = copy.deepcopy(self.full_grid)
        self.obstacles.clear()
        
        #self.current_config = rand.randint(0, 3) #prendo casualmente una delle varie mappe (PER QUANDO SARANNNO TUTTI PRONTI)
        self.current_config = 0

        # creo la lista di Obstacles e aggiorno la griglia
        for pos in self.configs[self.current_config]:
            obstacle = Obstacle("gray", pos[0], pos[1])
            self.obstacles.append(obstacle)
            self.delete_cell(pos)

    
    '''

    def is_ammissible(self, new_obstacle, snakes):
        for i in range(len(self.obstacles)):
            #controllo posizioni occupate in diagonale
            if ((new_obstacle.x_position == self.obstacles[i].x_position + 1 and new_obstacle.y_position == self.obstacles[i].y_position + 1) or \
                (new_obstacle.x_position == self.obstacles[i].x_position - 1 and new_obstacle.y_position == self.obstacles[i].y_position - 1) or \
                (new_obstacle.x_position == self.obstacles[i].x_position + 1 and new_obstacle.y_position == self.obstacles[i].y_position - 1) or \
                (new_obstacle.x_position == self.obstacles[i].x_position - 1 and new_obstacle.y_position == self.obstacles[i].y_position + 1) or \
                (new_obstacle.x_position == self.obstacles[i].x_position and new_obstacle.y_position == self.obstacles[i].y_position)):
                return False

        #facciamo in modo che non ci siano ostacoli immediatamente davanti lo snake
        for i in range(len(snakes)):
            head = snakes[i].get_body()[-1]
            if snakes[i].start_location == 'top-left':
                if (head[0] == new_obstacle.x_position and (head[1]== new_obstacle.y_position - 1 or head[1] == new_obstacle.y_position - 2)):
                    return False
            else:
                if (head[0] == new_obstacle.x_position and (head[1] == new_obstacle.y_position + 1 or head[1] == new_obstacle.y_position + 2)):
                    return False
        return True

    def is_overlapped(self, position, snakes): #snakes è una lista di stringhe (male male!!)
        for i in range(len(snakes)):
            for segment in snakes[i].body:
                if segment == position:
                    return True
        return False
    '''

    def delete_cell(self, del_key):
        self.grid.pop(del_key, None)
        for key in self.grid:
            if del_key in self.grid[key]:
                self.grid[key].remove(del_key)

    def get_obstacles(self):
        return copy.deepcopy(self.obstacles)

    def get_cycle(self):
        return copy.deepcopy(self.hamcycles[self.current_config])

    def get_grid_free_area(self):
        return (self.x_blocks * self.y_blocks) - len(self.obstacles)
            
class Obstacle:
    def __init__(self, color, x, y):
        self.color = color
        self.x_position = x
        self.y_position = y