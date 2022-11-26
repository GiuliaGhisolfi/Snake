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

    def spawn_obstacles(self, snakes):
        self.grid = copy.deepcopy(self.full_grid)
        self.obstacles.clear()
        num_obstacles = math.ceil(math.sqrt(self.x_blocks * self.y_blocks)) - 1
        for i in range(num_obstacles):
            while True:
                x_new = rand.randrange(1, self.x_blocks - 1)
                y_new = rand.randrange(1, self.y_blocks - 1)
                obstacle = Obstacle('gray', x_new, y_new)
                position = (x_new, y_new)
                if (self.is_ammissible(obstacle, snakes)) and (not self.is_overlapped(position, snakes)):
                    self.obstacles.append(obstacle)
                    self.delete_cell(position)
                    break

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

    def draw_cycle(self, game, window, cycle):
        self.grid_area = self.x_blocks * self.y_blocks
        direct = self.compute_hamilton_direction(cycle)
        add = math.floor(self.block_size / 2)

        for node in cycle:
            x, y = node
            value = cycle[node]
            dir = (direct[value - 1], direct[value])
            
            if dir == (0, 0) or dir == (1, 1): # RIGHT to RIGHT or LEFT to LEFT:
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size), (y * self.block_size + add), self.block_size, 1))
            if dir == (2, 2) or dir == (3, 3):  # DOWN to DOWN or UP to UP:
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size), 1, self.block_size))
            if dir == (1, 2) or dir == (3, 0):  # L to D or U to R
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size + add), 1, self.block_size / 2))
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size + add), self.block_size / 2, 1))
                
            if dir == (0, 2) or dir == (3, 1):  # R to D or U to L
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size + add), 1, self.block_size / 2))
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size), (y * self.block_size + add), self.block_size / 2, 1))
                
            if dir == (0, 3) or dir == (2, 1):  # R to U or D to L
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size), 1, self.block_size / 2))
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size), (y * self.block_size + add), self.block_size / 2, 1))
                
            if dir == (2, 0) or dir == (1, 3):  # D to R or L to U
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size), 1, self.block_size / 2))
                game.draw.rect(window, colors.WHITE,
                               ((x * self.block_size + add), (y * self.block_size + add), self.block_size / 2, 1))

    def is_ammissible(self, new_obstacle, snakes):
        for i in range(len(self.obstacles)):
            # controllo posizioni occupate in diagonale
            if ((new_obstacle.x_position == self.obstacles[i].x_position + 1 and new_obstacle.y_position == self.obstacles[i].y_position + 1) or
                (new_obstacle.x_position == self.obstacles[i].x_position - 1 and new_obstacle.y_position == self.obstacles[i].y_position - 1) or
                (new_obstacle.x_position == self.obstacles[i].x_position + 1 and new_obstacle.y_position == self.obstacles[i].y_position - 1) or
                (new_obstacle.x_position == self.obstacles[i].x_position - 1 and new_obstacle.y_position == self.obstacles[i].y_position + 1) or
                    (new_obstacle.x_position == self.obstacles[i].x_position and new_obstacle.y_position == self.obstacles[i].y_position)):
                return False

        # facciamo in modo che non ci siano ostacoli immediatamente davanti lo snake
        for i in range(len(snakes)):
            head = snakes[i].get_body()[-1]
            if snakes[i].start_location == 'top-left':
                if (head[0] == new_obstacle.x_position and (head[1] == new_obstacle.y_position - 1 or head[1] == new_obstacle.y_position - 2)):
                    return False
            else:
                if (head[0] == new_obstacle.x_position and (head[1] == new_obstacle.y_position + 1 or head[1] == new_obstacle.y_position + 2)):
                    return False
        return True

    # snakes è una lista di stringhe (male male!!)
    def is_overlapped(self, position, snakes):
        for i in range(len(snakes)):
            for segment in snakes[i].body:
                if segment == position:
                    return True
        return False

    def delete_cell(self, del_key):
        self.grid.pop(del_key, None)
        for key in self.grid:
            if del_key in self.grid[key]:
                self.grid[key].remove(del_key)

    def get_obstacles(self):
        return copy.deepcopy(self.obstacles)


class Obstacle:
    def __init__(self, color, x, y):
        self.color = color
        self.x_position = x
        self.y_position = y
