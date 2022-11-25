import copy
import random as rand
import math

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
                if  0 <= nx < self.x_blocks and 0 <= ny < self.y_blocks:
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
                if self.is_ammissible(obstacle, snakes) and not self.is_overlapped(position, snakes):
                    self.obstacles.append(obstacle)
                    self.delete_cell(position)
                    break

    def draw_obstacles(self, game, window):
        for i in range(len(self.obstacles)):
            game.draw.rect(
                window,
                self.obstacles[i].color,
                ((self.obstacles[i].x_position) * self.block_size +1 , (self.obstacles[i].y_position) * self.block_size +1, self.block_size-2, self.block_size-2))

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