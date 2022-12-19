import copy
import random as rand
import math
import colors
import gui
import pygame
from obstacles_configurations import Obstacles_configurations

class Grid:
    def __init__(self, size, x_blocks, y_blocks):
        self.size = size
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        x_pixel = size - (size % x_blocks)
        self.bounds = (x_pixel, x_pixel * y_blocks / x_blocks)
        self.block_size = x_pixel / x_blocks
        self.full_grid = self.build_grid()
        self.grid = copy.deepcopy(self.full_grid)
        self.obstacles = []

    def build_grid(self):
        '''builds the grid based on every node's neighboors'''
        def neighbors(x, y):
            '''returns every node's neighboors'''
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
        '''draw the obstacles'''
        for i in range(len(self.obstacles)):
            game.draw.rect(
                window,
                self.obstacles[i].color,
                ((self.obstacles[i].x_position) * self.block_size + 1, (self.obstacles[i].y_position) * self.block_size + 1, self.block_size-2, self.block_size-2))

    def draw_cycle(self, game, window, cycle, color, closed=True):

        # 

        points = []
        shift = self.block_size/2
        count = 0
        while count < len(cycle):
            for node in cycle:
                if cycle[node] == count:
                    points.append((node[0]*self.block_size + shift,
                            node[1] * self.block_size + shift))
                    count += 1
        if len(points) > 1:
            game.draw.lines(window, color, closed, points)

    def draw_path(self, game, window, items):
        '''draw the calculated path'''

        cycles = items[0]
        cl = items[1]
        closed = items[2]

        for i, c in enumerate(cycles):
            points = []
            shift = self.block_size/2
            for n in c:
                points.append((n[0]*self.block_size + shift, n[1] * self.block_size + shift))
            if len(points) > 1:
                game.draw.lines(window, cl[i], closed[i], points)

    def spawn_obstacles(self, obstacles):
        '''create the obstacle's configuration of the grid'''
        self.grid = copy.deepcopy(self.full_grid)
        self.obstacles.clear()
        self.current_config = obstacles

        # create the Obstacles' list and update the grid
        obc = Obstacles_configurations(self)
        for pos in obc.configs[self.current_config]:
            obstacle = Obstacle("gray", pos[0], pos[1])
            self.obstacles.append(obstacle)
            self.delete_cell(pos)

    def delete_cell(self, del_key):
        '''delete an entry on the grid dictionary'''
        self.grid.pop(del_key, None)
        for key in self.grid:
            if del_key in self.grid[key]:
                self.grid[key].remove(del_key)

    def get_obstacles(self):
        return copy.deepcopy(self.obstacles)

    def get_cycle(self, obstacles):
        if obstacles == "None": 
            self.current_config = 4
        obc = Obstacles_configurations(self)
        return copy.deepcopy(obc.hamcycles[self.current_config])

    def get_grid_free_area(self):
        return (self.x_blocks * self.y_blocks) - len(self.obstacles)
    
    def update_grid_dimensions(self, X, Y):
        self.x_blocks = X
        self.y_blocks = Y
        x_pixel = self.size-(self.size % self.x_blocks)
        self.bounds = (x_pixel, x_pixel*self.y_blocks/self.x_blocks)
        self.block_size = x_pixel/self.x_blocks
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
