import copy
import random as rand
import math
import colors


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
            },
            {
                (0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (0, 4): 4, (0, 5): 5, (0, 6): 6, (0, 7): 7, (0, 8): 8, (0, 9): 9, (0, 10): 10, (0, 11): 11, (0, 12): 12, (0, 13): 13, (0, 14): 14, (0, 15): 15,
                (1, 0): 213, (1, 1): 38, (1, 2): 37, (1, 3): 34, (1, 4): 33, (1, 5): 30, (1, 6): 29, (1, 7): 26, (1, 8): 25, (1, 9): 22, (1, 10): 21, (1, 11): 20, (1, 12): 19, (1, 13): 18, (1, 14): 17, (1, 15): 16,
                (2, 0): 212, (2, 1): 39, (2, 2): 36, (2, 3): 35, (2, 4): 32, (2, 5): 31, (2, 6): 28, (2, 7): 27, (2, 8): 24, (2, 9): 23, (2, 10): 50, (2, 11): 51, (2, 12): 52, (2, 13): 53, (2, 14): 54, (2, 15): 55,
                (3, 0): 211, (3, 1): 40, (3, 2): 41, (3, 3): 42, (3, 4): 43, (3, 5): 44, (3, 6): 45, (3, 7): 46, (3, 8): 47, (3, 9): 48, (3, 10): 49, (3, 14): 57, (3, 15): 56,
                (4, 0): 210, (4, 1): 209, (4, 2): 208, (4, 6): 140, (4, 7): 139, (4, 8): 132, (4, 9): 131, (4, 10): 130, (4, 14): 58, (4, 15): 59,
                (5, 1): 206, (5, 2): 207, (5, 3): 194, (5, 4): 193, (5, 5): 192, (5, 6): 141, (5, 7): 138, (5, 8): 133, (5, 9): 128, (5, 10): 129, (5, 14): 61, (5, 15): 60,
                (6, 1): 205, (6, 2): 196, (6, 3): 195, (6, 4): 190, (6, 5): 191, (6, 6): 142, (6, 7): 137, (6, 8): 134, (6, 9): 127, (6, 10): 70, (6, 11): 69, (6, 12): 68, (6, 13): 67, (6, 14): 62, (6, 15): 63,
                (7, 1): 204, (7, 2): 197, (7, 3): 188, (7, 4): 189, (7, 5): 144, (7, 6): 143, (7, 7): 136, (7, 8): 135, (7, 9): 126, (7, 10): 71, (7, 11): 74, (7, 12): 75, (7, 13): 66, (7, 14): 65, (7, 15): 64,
                (8, 0): 202, (8, 1): 203, (8, 2): 198, (8, 3): 187, (8, 4): 186, (8, 5): 145, (8, 8): 124, (8, 9): 125, (8, 10): 72, (8, 11): 73, (8, 12): 76, (8, 13): 77, (8, 14): 78, (8, 15): 79,
                (9, 0): 201, (9, 1): 200, (9, 2): 199, (9, 3): 184, (9, 4): 185, (9, 5): 146, (9, 8): 123, (9, 9): 122, (9, 11): 104, (9, 12): 103, (9, 13): 92, (9, 14): 91, (9, 15): 80,
                (10, 0): 176, (10, 1): 177, (10, 2): 178, (10, 3): 183, (10, 4): 182, (10, 5): 147, (10, 6): 148, (10, 7): 149, (10, 8): 120, (10, 9): 121, (10, 11): 105, (10, 12): 102, (10, 13): 93, (10, 14): 90, (10, 15): 81,
                (11, 0): 175, (11, 1): 174, (11, 2): 179, (11, 3): 180, (11, 4): 181, (11, 5): 158, (11, 6): 157, (11, 7): 150, (11, 8): 119, (11, 9): 118, (11, 11): 106, (11, 12): 101, (11, 13): 94, (11, 14): 89, (11, 15): 82,
                (12, 0): 172, (12, 1): 173, (12, 5): 159, (12, 6): 156, (12, 7): 151, (12, 8): 116, (12, 9): 117, (12, 11): 107, (12, 12): 100, (12, 13): 95, (12, 14): 88, (12, 15): 83,
                (13, 0): 171, (13, 1): 168, (13, 2): 167, (13, 3): 164, (13, 4): 163, (13, 5): 160, (13, 6): 155, (13, 7): 152, (13, 8): 115, (13, 9): 112, (13, 10): 111, (13, 11): 108, (13, 12): 99, (13, 13): 96, (13, 14): 87, (13, 15): 84,
                (14, 0): 170, (14, 1): 169, (14, 2): 166, (14, 3): 165, (14, 4): 162, (14, 5): 161, (14, 6): 154, (14, 7): 153, (14, 8): 114, (14, 9): 113, (14, 10): 110, (14, 11): 109, (14, 12): 98, (14, 13): 97, (14, 14): 86, (14, 15): 85
            },
            {

            },
            {

            }
        ]

    def build_grid(self):
        def neighbors(x, y):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for (dx, dy) in directions:
                (nx, ny) = (x + dx, y + dy)
                if 0 <= nx < self.x_blocks and 0 <= ny < self.y_blocks:
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
                ((self.obstacles[i].x_position) * self.block_size + 1, (self.obstacles[i].y_position) * self.block_size + 1, self.block_size-2, self.block_size-2))

    def hamilton_direction(self, x, y, xprec, yprec):
        if x == xprec + 1:
            return 0  # RIGHT
        elif x == xprec - 1:
            return 1  # LEFT
        elif y == yprec + 1:
            return 2  # DOWN
        elif y == yprec - 1:
            return 3  # UP

    def compute_hamilton_direction(self, cycle):
        # direct[i] = direction from node with value = i to node (i + 1) in hamilton cycle
        direct = []
        for value in range(self.grid_area):
            for node in cycle:
                if cycle[node] == value:
                    curr = node  # chiave del nodo che ha come valore value
                    break
            x, y = curr
            if value != 0:
                direct.append(self.hamilton_direction(x, y, xprec, yprec))
            else:
                x0 = x
                y0 = y
            xprec = x
            yprec = y

        direct.append(self.hamilton_direction(x0, y0, xprec, yprec))
        return direct

    def draw_cycle(self, game, window, cycle, ham_cycle_changed):
        self.grid_area = self.get_grid_free_area()
        if ham_cycle_changed:
            self.direct = self.compute_hamilton_direction(cycle)
        add = math.floor(self.block_size / 2)

        for node in cycle:
            x, y = node
            value = cycle[node]
            dir = (self.direct[value - 1], self.direct[value])
            
            if dir == (0, 0) or dir == (1, 1):  # RIGHT to RIGHT or LEFT to LEFT:
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size), (y * self.block_size + add), self.block_size + 1, 1))

            if dir == (2, 2) or dir == (3, 3):  # DOWN to DOWN or UP to UP:
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size), 1, self.block_size + 1))

            if dir == (1, 2) or dir == (3, 0):  # L to D or U to R
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size + add), 1, (self.block_size / 2) + 1))
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size + add), (self.block_size / 2) + 1, 1))

            if dir == (0, 2) or dir == (3, 1):  # R to D or U to L
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size + add), 1, (self.block_size / 2) + 1))
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size), (y * self.block_size + add), (self.block_size / 2) + 1, 1))

            if dir == (0, 3) or dir == (2, 1):  # R to U or D to L
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size), 1, (self.block_size / 2) + 1))
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size), (y * self.block_size + add), (self.block_size / 2) + 1, 1))

            if dir == (2, 0) or dir == (1, 3):  # D to R or L to U
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size), 1, (self.block_size / 2) + 1))
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size + add), (self.block_size / 2) + 1, 1))

    
    def spawn_obstacles(self):
        self.grid = copy.deepcopy(self.full_grid)
        self.obstacles.clear()
        
        #self.current_config = rand.randint(0, 3) #prendo casualmente una delle varie mappe (PER QUANDO SARANNNO TUTTI PRONTI)
        self.current_config = rand.randint(0, 1)

        # creo la lista di Obstacles e aggiorno la griglia
        for pos in self.configs[self.current_config]:
            obstacle = Obstacle("gray", pos[0], pos[1])
            self.obstacles.append(obstacle)
            self.delete_cell(pos)


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
