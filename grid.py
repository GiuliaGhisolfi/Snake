import copy
import random as rand
import math
import colors
import button
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
        '''returns new direcrtion based on the hamiltonian cycle followed by the snake'''
        direct = [] # direct[i] = direction from node with value = i to node (i + 1) in hamilton cycle
        for value in range(self.grid_area):
            for node in cycle:
                if cycle[node] == value:
                    curr = node  # node's key where node's value = value
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
    
    def hamilton_direction(self, x, y, xprec, yprec):
        if x == xprec + 1:
            return 0  # RIGHT
        elif x == xprec - 1:
            return 1  # LEFT
        elif y == yprec + 1:
            return 2  # DOWN
        elif y == yprec - 1:
            return 3  # UP

    def draw_cycle(self, game, window, cycle, ham_cycle_changed):
        '''draw the path of the hamiltonian cycle'''
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

    def draw_path(self, game, window, cycles, cl, closed):
        '''draw the calculated path in greedy strategy'''
        for i, c in enumerate(cycles):
            points = []
            shift = self.block_size/2
            for n in c:
                points.append((n[0]*self.block_size + shift, n[1] * self.block_size + shift))
            if len(points) > 1:
                game.draw.lines(window, cl[i], closed[i], points)

    def spawn_obstacles(self):
        '''create the obstacle's configuration of the grid'''
        self.grid = copy.deepcopy(self.full_grid)
        self.obstacles.clear()
        self.current_config = button.OBSTACLES

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

    def get_cycle(self):
        if button.OBSTACLES == "None": 
            self.current_config = 4
        obc = Obstacles_configurations(self)
        return copy.deepcopy(obc.hamcycles[self.current_config])

    def get_grid_free_area(self):
        return (self.x_blocks * self.y_blocks) - len(self.obstacles)
    
    def update_grid_dimensions(self,X,Y):
        self.x_blocks = X
        self.y_blocks = Y
        x_pixel = self.size-(self.size % self.x_blocks)
        self.bounds = (x_pixel, x_pixel*self.y_blocks/self.x_blocks)
        self.block_size = x_pixel/self.x_blocks
        self.full_grid = self.build_grid()
        self.grid = copy.deepcopy(self.full_grid)
        pygame.display.quit()
        pygame.init()
        button.window = pygame.display.set_mode(self.bounds)

class Obstacle:
    def __init__(self, color, x, y):
        self.color = color
        self.x_position = x
        self.y_position = y
