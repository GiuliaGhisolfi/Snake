import random

class Food:
    def __init__(self, color, block_size, x_chessboard, y_chessboard, snake_body, bot_body):
        self.color = color
        self.block_size = block_size
        self.x_chessboard = x_chessboard
        self.y_chessboard = y_chessboard
        self.x_old = -1
        self.y_old = -1
        self.respawn(snake_body, bot_body)


    def draw(self, game, window):
        game.draw.rect(window, self.color, (self.x, self.y, self.block_size, self.block_size))


    def respawn(self, snake_body, bot_body):
        while True:
            check = 0
            self.x = random.randint(1, self.x_chessboard-2) * self.block_size
            for segment in snake_body:
                if segment[0] == self.x:
                    check = 1
            for segment in bot_body:
                if segment[0] == self.x:
                    check = 1
            if self.x != self.x_old and check == 0:
                break
            
        while True:
            check = 0
            self.y = random.randint(1, self.y_chessboard-2) * self.block_size
            for segment in snake_body:
                if segment[1] == self.y:
                    check = 1
            for segment in bot_body:
                if segment[1] == self.y:
                    check = 1
            if self.y != self.y_old and check == 0:
                break
            
        self.x_old = self.x
        self.y_old = self.y