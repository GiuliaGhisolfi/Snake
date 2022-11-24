import random as rand
import threading
import copy

#NON threadSafe
class Food:
    def __init__(self, color):
        self.color = color #immutabile
        self.position = [] #da lockare!

    def draw(self, game, window, grid):

        [x,y] = self.coord_from_graph(grid)
        game.draw.rect(
            window,
            self.color,
            (x+1, y+1, grid.block_size-2, grid.block_size-2))
        
    def coord_from_graph(self, grid):
        node = self.position[0]

        #chars = ['(', ')']
        #node = node.translate(str.maketrans({ord(char): '' for char in chars}))
        #node = node.split(',')
        #for i in range(2): node[i] = int(node[i])
        return (node[0]*grid.block_size, node[1]*grid.block_size)

    def is_overlapped(self, position, snakes, obstacles):
        for s in snakes:
            for segment in s.body:
                if segment == position:
                    return True
        for p in obstacles.positions: #dopo facciamo la deepcopy
            if position == p: #GETTER!!!!!!!!
                return True
        return False

    def respawn(self, snakes, grid, obstacles):
        while True:
            x_new = rand.randrange(0, grid.x_blocks)
            y_new = rand.randrange(0, grid.y_blocks)
            
            new_position = x_new, y_new
            if [new_position] != self.position and not self.is_overlapped(new_position, snakes, obstacles):
                self.position = [new_position]
                break

    def get_positions(self):
        return copy.deepcopy(self.position)
    def fast_get_positions(self):
        return self.position #attenzione, rompe i principi di Barbara :(

#Threadsafe
class LockedFood(Food):
    def __init__(self, color):
        super().__init__(color)
        self.lock = threading.RLock()

    def integer_from_string(self, grid):
        self.lock.acquire()
        try:
            ret = super().integer_from_string(grid)
        finally: self.lock.release()
        return ret

    def respawn(self, snakes, grid):
        self.lock.acquire()
        try:
            super().respawn(snakes, grid)
        finally: self.lock.release()

    def get_positions(self):
        self.lock.acquire()
        try:
            pos = super().get_positions()
        finally: self.lock.release()
        return pos
    
    def fast_get_positions(self):
        self.lock.acquire()
        try:
            pos = super().get_positions()
        finally: self.lock.release()
        return pos
