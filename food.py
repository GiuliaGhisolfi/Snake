from random import randint
import threading
class Food:
    def __init__(self, color):
        self.color = color
        self.position = []

    def draw(self, game, window, grid):
        [x,y] = self.integer_from_string(grid)
        game.draw.rect(
            window,
            self.color,
            (x+1, y+1, grid.block_size-2, grid.block_size-2))
        
    def integer_from_string(self, grid):
        node = self.position[0]
        chars = ['(', ')']
        node = node.translate(str.maketrans({ord(char): '' for char in chars}))
        node = node.split(',')
        for i in range(2):
            node[i] = int(node[i])
        return [int(node[0])*grid.block_size, int(node[1])*grid.block_size]

    def is_overlapped(self, position, snakes):
        for i in range(len(snakes)):
            for segment in snakes[i].body:
                if segment == position:
                    return True
        return False

    def respawn(self, snakes, grid):
        while True:
            x_new = randint(1, grid.x_blocks-2)
            y_new = randint(1, grid.y_blocks-2)
            
            new_position = "(%d,%d)" % (x_new, y_new)
            if [new_position] != self.position and not self.is_overlapped(new_position, snakes):
                self.position = [new_position]
                break

    def get_positions(self):

        pos = self.position
        return pos