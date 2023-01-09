import copy
import src.gui as gui
import pygame
from src.obstacles_configs import ObstaclesConfig

class Grid:
    """This class implements the game grid."""
    
    def __init__(self, grid_size, x_blocks, y_blocks):
        self.grid_size = grid_size
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        x_pixel = grid_size - (grid_size % x_blocks)
        self.bounds = (x_pixel, x_pixel * y_blocks / x_blocks)
        self.block_size = x_pixel / x_blocks
        self.full_grid = self.build_grid()
        self.grid = copy.deepcopy(self.full_grid)
        self.obstacles = []

    def build_grid(self):
        """Builds the grid."""
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
        """Draws the obstacles."""
        for i in range(len(self.obstacles)):
            game.draw.rect(
                window,
                self.obstacles[i].color,
                (
                    (self.obstacles[i].x_position) * self.block_size + 1, 
                    (self.obstacles[i].y_position) * self.block_size + 1, 
                    self.block_size-2,
                    self.block_size-2
                )
            )

    def draw_cycle(self, game, window, cycle, color, closed=True):
        """Draws the Hamiltonian cycle."""
        points = []
        shift = self.block_size/2
        count = 0
        while count < len(cycle):
            for node in cycle:
                if cycle[node] == count:
                    points.append((
                            node[0]*self.block_size + shift,
                            node[1] * self.block_size + shift
                        ))
                    count += 1
        if len(points) > 1:
            game.draw.lines(window, color, closed, points)

    def draw_path(self, game, window, items):
        """Draws the path the snake is going to follow."""
        cycles = items[0]
        colors = items[1]
        closed = items[2]
        for i, c in enumerate(cycles):
            points = []
            shift = self.block_size/2
            for n in c:
                points.append((
                    n[0]*self.block_size + shift,
                    n[1] * self.block_size + shift
                ))
            if len(points) > 1:
                game.draw.lines(window, colors[i], closed[i], points)

    def spawn_obstacles(self, obstacles):
        """Sets the obstacles on the grid."""
        if obstacles == 'None':
            return
        self.grid = copy.deepcopy(self.full_grid)
        self.obstacles.clear()
        self.current_config = obstacles

        obc = ObstaclesConfig(self)
        for pos in obc.configs[int(self.current_config)]:
            obstacle = Obstacle("gray", pos[0], pos[1])
            self.obstacles.append(obstacle)
            self.delete_cell(pos)

    def delete_cell(self, cell_to_del):
        """Deletes a cell on the grid."""
        self.grid.pop(cell_to_del, None)
        for cell in self.grid:
            if cell_to_del in self.grid[cell]:
                self.grid[cell].remove(cell_to_del)

    def get_obstacles(self):
        return copy.deepcopy(self.obstacles)

    def get_cycle(self, obstacles):
        if obstacles == "None": 
            self.current_config = 4
        obc = ObstaclesConfig(self)
        return copy.deepcopy(obc.hamcycles[int(self.current_config)])

    def get_grid_free_area(self):
        return (self.x_blocks * self.y_blocks) - len(self.obstacles)
    
    def update_grid_dimensions(self, x_blocks, y_blocks):
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        x_pixel = self.grid_size - (self.grid_size % self.x_blocks)
        self.bounds = (x_pixel, x_pixel * self.y_blocks / self.x_blocks)
        self.block_size = x_pixel / self.x_blocks
        self.full_grid = self.build_grid()
        self.grid = copy.deepcopy(self.full_grid)
        pygame.display.quit()
        pygame.init()
        gui.window = pygame.display.set_mode(self.bounds)

class Obstacle:
    def __init__(self, color, x, y):
        self.color = color
        self.x_position = x
        self.y_position = y