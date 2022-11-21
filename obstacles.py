import random as rand
import math 

class Obstacles:

    def __init__(self, color):
        self.color = color        
        self.positions = []

    def draw(self, game, window, grid):
        for i in range(len(self.positions)):
            game.draw.rect(
                window,
                self.color,
                ((self.positions[i][0])*grid.block_size +1 , (self.positions[i][1])*grid.block_size +1, grid.block_size-2, grid.block_size-2))
     
    
    def spawn(self, snakes, grid):
        self.positions.clear()
        num_obstacles = math.ceil(math.sqrt(grid.x_blocks*grid.y_blocks))-1
        for i in range(num_obstacles):
            while True:
                x_new = rand.randrange(1, grid.x_blocks-1)
                y_new = rand.randrange(1, grid.y_blocks-1)
                position = (x_new, y_new)
                str_position = "(%d,%d)" % (x_new, y_new)
                if self.is_ammissible(position) and not self.is_overlapped(str_position,snakes):
                    self.positions.append(position)
                    break


    def is_ammissible(self,position):
        for i in range(len(self.positions)):
            #controllo posizioni occupate in diagonale
            if ((position[0] == self.positions[i][0] + 1 and position[1] == self.positions[i][1] + 1) or \
                (position[0] == self.positions[i][0] - 1 and position[1] == self.positions[i][1] - 1) or \
                (position[0] == self.positions[i][0] + 1 and position[1] == self.positions[i][1] - 1) or \
                (position[0] == self.positions[i][0] - 1 and position[1] == self.positions[i][1] + 1) or \
                (position[0] == self.positions[i][0] and position[1] == self.positions[i][1])):
                return False
        return True

    def is_overlapped(self, position, snakes): #snakes è una lista di stringhe
        for i in range(len(snakes)):
            for segment in snakes[i].body:
                if segment == position:
                    return True
        return False