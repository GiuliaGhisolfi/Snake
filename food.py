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
            (self.x, self.y, chessboard.block_size, chessboard.block_size))

    def is_overlapped(self, coordinate, axis, snakes):
        for i in range(len(snakes)):
            for segment in snakes[i].body:
                if segment[axis] == coordinate:
                    return True
        return False

    def respawn(self, snakes, chessboard):
        while True:
            x_new = randint(1, chessboard.x_blocks-2)*chessboard.block_size
            if x_new != self.x and not self.is_overlapped(x_new, 0, snakes):
                break
        self.x = x_new

        while True:
            y_new = randint(1, chessboard.y_blocks-2)*chessboard.block_size
            if y_new != self.y and not self.is_overlapped(y_new, 1, snakes):
                break
        self.y = y_new