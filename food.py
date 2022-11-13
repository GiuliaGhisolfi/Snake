from random import randint
import threading


#threadsafe
class Food:
    def __init__(self, color):
        self.color = color #immutabile
        self.position = [] #da lockare!

        self.lock = threading.RLock()

    def draw(self, game, window, grid):

        [x,y] = self.integer_from_string(grid)
        game.draw.rect(
            window,
            self.color,
            (x+1, y+1, grid.block_size-2, grid.block_size-2))
        
    def integer_from_string(self, grid):
        self.lock.acquire()
        try:
            node = self.position[0]
            chars = ['(', ')']
            node = node.translate(str.maketrans({ord(char): '' for char in chars}))
            node = node.split(',')
            for i in range(2):
                node[i] = int(node[i])
        finally: self.lock.release()
        return [int(node[0])*grid.block_size, int(node[1])*grid.block_size]

    def is_overlapped(self, position, snakes):
        for i in range(len(snakes)):
            for segment in snakes[i].body:
                if segment == position:
                    return True
        return False

    def respawn(self, snakes, grid):
        self.lock.acquire()
        try:
            while True:
                x_new = randint(1, grid.x_blocks-2)
                y_new = randint(1, grid.y_blocks-2)
                
                new_position = "(%d,%d)" % (x_new, y_new)
                if [new_position] != self.position and not self.is_overlapped(new_position, snakes):
                    self.position = [new_position]
                    break
        finally: self.lock.release()

    def get_positions(self):
        self.lock.acquire()
        pos = self.position
        self.lock.release()
        return pos