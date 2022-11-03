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

    def respawn(self, snake_body, bot_body, chessboard):
        while True:
            overlap = False
            x_new = randint(1, chessboard.x_blocks-2)*chessboard.block_size
            for segment in snake_body:
                if segment[0] == x_new:
                    overlap = True
                    break
            if overlap:
                continue
            for segment in bot_body:
                if segment[0] == x_new:
                    overlap = True
                    break
            if x_new != self.x and not overlap:
                break
        self.x = x_new

        while True:
            overlap = False
            y_new = randint(1, chessboard.y_blocks-2)*chessboard.block_size
            for segment in snake_body:
                if segment[1] == y_new:
                    overlap = True
                    break
            if overlap:
                continue
            for segment in bot_body:
                if segment[1] == y_new:
                    overlap = True
                    break
            if y_new != self.y and not overlap:
                break
        self.y = y_new