from random import randint

class Food:
    def __init__(self, color):
        self.color = color
        self.x = -1
        self.y = -1

    def draw(self, game, window, chessboard):
        game.draw.rect(
            window,
            self.color,
            (self.x+1, self.y+1, chessboard.block_size-2, chessboard.block_size-2))

    def is_overlapped(self, x, y, snakes):
        for i in range(len(snakes)):
            for segment in snakes[i].body:
                if segment[0] == x and segment[1] == y:
                    return True
        return False

    def respawn(self, snakes, chessboard):
        while True:
            x_new = randint(1, chessboard.x_blocks-2)*chessboard.block_size
            y_new = randint(1, chessboard.y_blocks-2)*chessboard.block_size
            if y_new != self.y and x_new != self.x and not self.is_overlapped(x_new, y_new, snakes):
                self.x = x_new
                self.y = y_new
                break