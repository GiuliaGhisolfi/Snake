from directions import Directions

class Snake:
    def __init__(self, color, start_location):
        self.color = color
        self.start_location = start_location
    
    def respawn(self, chessboard):
        self.length = 3
        if self.start_location == "top-left":
            self.body = [
                (3*chessboard.block_size, 2*chessboard.block_size), \
                (3*chessboard.block_size, 3*chessboard.block_size), \
                (3*chessboard.block_size, 4*chessboard.block_size)]
            self.direction = Directions.DOWN
        if self.start_location == "bottom-right":
            self.body = [
                ((chessboard.x_blocks-4)*chessboard.block_size, \
                (chessboard.y_blocks-3)*chessboard.block_size), \
                ((chessboard.x_blocks-4)*chessboard.block_size, \
                    (chessboard.y_blocks-4)*chessboard.block_size), \
                ((chessboard.x_blocks-4)*chessboard.block_size, \
                    (chessboard.y_blocks-5)*chessboard.block_size)]
            self.direction = Directions.UP

    def draw(self, game, window, chessboard):
        for segment in self.body:
            game.draw.rect(
                window, 
                self.color, 
                (segment[0], 
                    segment[1], 
                    chessboard.block_size, 
                    chessboard.block_size))

    def move(self, direction, chessboard):
        self.__steer(direction)

        curr_head = self.body[-1]
        if self.direction == Directions.DOWN:
            next_head = (curr_head[0], curr_head[1] + chessboard.block_size)
            self.body.append(next_head)
        elif self.direction == Directions.UP:
            next_head = (curr_head[0], curr_head[1] - chessboard.block_size)
            self.body.append(next_head)
        elif self.direction == Directions.RIGHT:
            next_head = (curr_head[0] + chessboard.block_size, curr_head[1])
            self.body.append(next_head)
        elif self.direction == Directions.LEFT:
            next_head = (curr_head[0] - chessboard.block_size, curr_head[1])
            self.body.append(next_head)

        if self.length < len(self.body):
            self.body.pop(0)

    def __steer(self, direction):
        if direction == None:
            return
        if self.direction == Directions.DOWN and direction != Directions.UP:
            self.direction = direction
        elif self.direction == Directions.UP and direction != Directions.DOWN:
            self.direction = direction
        elif self.direction == Directions.LEFT and direction != Directions.RIGHT:
            self.direction = direction
        elif self.direction == Directions.RIGHT and direction != Directions.LEFT:
            self.direction = direction

    def eat(self):
        self.length += 1

    def can_eat(self, food):
        head = self.body[-1]
        return head[0] == food.x and head[1] == food.y

    def check_tail_collision(self):
        head = self.body[-1]
        for i in range(len(self.body) - 1):
            segment = self.body[i]
            if head[0] == segment[0] and head[1] == segment[1]:
                return True
        return False

    def check_adversarial_collision(self, adversarial_body):
        head = self.body[-1]
        for i in range(len(adversarial_body)):
            segment = adversarial_body[i]
            if head[0] == segment[0] and head[1] == segment[1]:
                return True
        return False

    def check_bounds(self, chessboard):
        head = self.body[-1]
        if head[0] >= chessboard.bounds[0] or \
            head[1] >= chessboard.bounds[1] or \
            head[0] < 0 or \
            head[1] < 0:
            return True
        return False
