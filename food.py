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

    def is_overlapped(self, position, snakes, grid):
        for s in snakes:
            for segment in s.get_body():
                if segment == position:
                    return True
        for p in grid.get_obstacles():
            obstacle = (p.x_position, p.y_position)
            if position == obstacle: #GETTER!!!!!!!!
                return True
        return False

    def respawn(self, snakes, grid):
        def distance(n1, n2):
            return abs(n1[0]-n2[0]) + abs(n1[0] - n2[0])

        nodes = list(grid.grid.keys())
        rand.shuffle(nodes)
        
        scartati = []
        for n in nodes:
            skip = False
            for s in snakes:
                if distance(n, s.get_body()[1]) <= 1:
                    skip = True
                    scartati.append(n)
            if n != self.position and not self.is_overlapped(n, snakes, grid):
                self.position = [n]
                return

        rand.shuffle(scartati)
        self.position = [scartati[0]]

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