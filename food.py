import random

class Food:
    block_size = None
    color = (255,0,0) 
    ## verde: (0,255,0)
    
    x = 120;
    y = 80; ## posizione iniziale food
    ## posizione deve essere multiplo di 20 (per coerenza con dimensioni snake)
    ## bisogna randomizzare anche questa (?)
    
    bouds = None


    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds


    def draw(self, game, window):
        game.draw.rect(window, self.color, (self.x, self.y, self.block_size, self.block_size))


    def respawn(self):
        blocks_in_x = int((self.bounds[0])/self.block_size) ##aggiunto integer
        blocks_in_y = int((self.bounds[1])/self.block_size)
        self.x = random.randint(1, blocks_in_x - 2) * self.block_size
        self.y = random.randint(1, blocks_in_y - 2) * self.block_size ## mele non possono stare sul bordo (matrice numerata da 0)