from directions import Directions
import threading
import copy

class Snake:
    def __init__(self, color=(0, 190, 80), start_location="top-left"):
        self.color = color  # immutabile
        self.start_location = start_location  # da lockare!

    def respawn(self, grid):
        self.length = 3
        if self.start_location == "top-left":
            self.body = [(3, 2),
                         (3, 3),
                         (3, 4)]
            self.direction = Directions.DOWN
        if self.start_location == "bottom-right":
            self.body = [((grid.x_blocks-4), (grid.y_blocks-4)),
                         ((grid.x_blocks-4), (grid.y_blocks-5)),
                         ((grid.x_blocks-4), (grid.y_blocks-6))]
            self.direction = Directions.UP
    
    def coord_from_graph(self, grid):
        body_coord = []
        for node in self.get_body():
            body_coord[len(body_coord):] = [
                (int(node[0])*grid.block_size, int(node[1])*grid.block_size)]
        return body_coord

    def draw(self, game, window, grid):
        # riduciamo il tempo dello snake lockato? o preferiamo la rapidità?
        body_coord = self.coord_from_graph(grid)

        bsize = grid.block_size
        head = body_coord[-1]
        tail = body_coord[0]

        # Draw tail
        game.draw.rect(window, self.color,
                       (tail[0]+1, tail[1]+1, bsize-2, bsize-2))
        prev = (body_coord[0][0], body_coord[0][1])
        # Draw the rest of the body
        for segment in body_coord[1:]:
            if segment[0] > prev[0]:
                game.draw.rect(window, self.color,
                               (segment[0]-1, segment[1]+1, bsize, bsize-2))
            elif segment[0] < prev[0]:
                game.draw.rect(window, self.color,
                               (segment[0]+1, segment[1]+1, bsize, bsize-2))
            elif segment[1] > prev[1]:
                game.draw.rect(window, self.color,
                               (segment[0]+1, segment[1]-1, bsize-2, bsize))
            elif segment[1] < prev[1]:
                game.draw.rect(window, self.color,
                               (segment[0]+1, segment[1]+1, bsize-2, bsize))
            prev = (segment[0], segment[1])
        # Draw eyes
        black = (0, 0, 0)
        eye_size = bsize/6

        if self.direction == Directions.UP or self.direction == Directions.DOWN:
            eye1_x = head[0]+1/3*bsize-eye_size/2
            eye2_x = head[0]+2/3*bsize-eye_size/2
            eye1_y = eye2_y = head[1]+1/2*bsize-eye_size/2
        else:
            eye1_x = eye2_x = head[0]+1/2*bsize-eye_size/2
            eye1_y = head[1]+1/3*bsize-eye_size/2
            eye2_y = head[1]+2/3*bsize-eye_size/2

        game.draw.rect(window, black, (eye1_x, eye1_y, eye_size, eye_size))
        game.draw.rect(window, black, (eye2_x, eye2_y, eye_size, eye_size))

    def move(self, direction, food):

        

        self.__steer(direction)
        x, y = self.body[-1]

        if self.direction == Directions.DOWN:
            y = y + 1
        elif self.direction == Directions.UP:
            y = y - 1
        elif self.direction == Directions.RIGHT:
            x = x + 1
        elif self.direction == Directions.LEFT:
            x = x - 1

        next_head = (x, y)
        self.body.append(next_head)

        mangiato = self.can_eat(food)
        if mangiato: self.eat()

        if self.length < len(self.body):
            self.body.pop(0)

        return mangiato

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
        return self.body[-1] == food.position  # confronto tra nodi

    def tail_collision(self):
        head = self.body[-1]
        for segment in self.body[:-1]:
            if head == segment:
                return True
        return False

    def adversarial_collision(self, adversarial_body):
        head = self.body[-1]
        for segment in adversarial_body:
            if head == segment:
                return True
        return False

    def bounds_collision(self, grid):
        head = self.body[-1]
        if head not in grid.grid:
            return True
        return False

    def get_body(self):
        return copy.deepcopy(self.body)

    def fast_get_body(self):  # attenzione, rompe i principi di Barbara :(
        return self.body

    def dir_to_cell(self, cell):
        head = self.body[-1]
        if cell[0] < head[0]:  # x shift
            return Directions.LEFT
        elif cell[0] > head[0]:
            return Directions.RIGHT
        elif cell[1] < head[1]:  # y shift
            return Directions.UP
        else:
            return Directions.DOWN

class LockedSnake(Snake):
    def __init__(self, color=(0, 190, 80), start_location="top-left"):

        super().__init__(color, start_location)
        self.lock = threading.RLock()

    def respawn(self, grid):
        self.lock.acquire()
        try:
            super().respawn(grid)
        finally:
            self.lock.release()

    def draw(self, game, window, grid):
        # riduciamo il tempo dello snake lockato? o preferiamo la rapidità?
        self.lock.acquire()
        try:
            super().draw(game, window, grid)
        finally:
            self.lock.release()

    def move(self, direction):
        self.lock.acquire()
        try:
            super().move(direction)
        finally:
            self.lock.release()

    def __steer(self, direction):
        self.lock.acquire()
        try:
            super().__steer(direction)
        finally:
            self.lock.release()

    def eat(self):
        self.lock.acquire()
        try:
            super().eat()
        finally:
            self.lock.release()

    def can_eat(self, food):
        self.lock.acquire()
        try:
            ret = super().can_eat(food)
        finally:
            self.lock.release()
        return ret  # confronto tra nodi

    def tail_collision(self):
        self.lock.acquire()
        try:
            ret = super().tail_collision()
        finally:
            self.lock.release()
        return ret

    def adversarial_collision(self, adversarial_body):
        self.lock.acquire()
        try:
            ret = super().adversarial_collision(adversarial_body)
        finally:
            self.lock.release()
        return ret

    def bounds_collision(self, grid):
        self.lock.acquire()
        try:
            ret = super().bounds_collision(grid)
        finally:
            self.lock.release()
        return ret

    def get_body(self):
        self.lock.acquire()
        try:
            ret = super().get_body()
        finally:
            self.lock.release()
        return ret

    def fast_get_body(self):
        self.lock.acquire()
        try:
            ret = copy.deepcopy(super().fast_get_body())
        finally:
            self.lock.release()
        return ret
