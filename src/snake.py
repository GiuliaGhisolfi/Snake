import copy
from src.directions import Directions
import src.colors as colors

class Snake:
    """This class implements the snake."""
    
    def __init__(self, color = colors.GREEN):
        self.color = color

    def respawn(self):
        """Respawn the snake at its starting position."""
        self.length = 3
        self.body = [(0, 0), (0, 1), (0, 2)]
        self.direction = Directions.DOWN
    
    def coord_from_graph(self, grid):
        """Return snake's body coordinates on the grid."""
        body_coord = []
        for node in self.get_body():
            body_coord[len(body_coord):] = [
                (int(node[0]) * grid.block_size, int(node[1]) * grid.block_size)
            ]
        return body_coord

    def draw(self, game, window, grid):
        """Draws the snake."""
        body_coord = self.coord_from_graph(grid)
        bsize = grid.block_size
        head = body_coord[-1]
        tail = body_coord[0]

        # Draw the tail
        game.draw.rect(
            window,
            self.color,
            (tail[0]+1, tail[1]+1, bsize-2, bsize-2)
        )
        prev = (body_coord[0][0], body_coord[0][1])

        # Draw the rest of the body
        for segment in body_coord[1:]:
            if segment[0] > prev[0]:
                game.draw.rect(
                    window,
                    self.color,
                    (segment[0]-1, segment[1]+1, bsize, bsize-2)
                )
            elif segment[0] < prev[0]:
                game.draw.rect(
                    window,
                    self.color,
                    (segment[0]+1, segment[1]+1, bsize, bsize-2)
                )
            elif segment[1] > prev[1]:
                game.draw.rect(
                    window,
                    self.color,
                    (segment[0]+1, segment[1]-1, bsize-2, bsize)
                )
            elif segment[1] < prev[1]:
                game.draw.rect(
                    window,
                    self.color,
                    (segment[0]+1, segment[1]+1, bsize-2, bsize)
                )
            prev = (segment[0], segment[1])
        
        # Draw the eyes
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
        """Moves the snake on the grid."""
        # change direction
        self.steer(direction)

        # get next head position
        x_head, y_head = self.body[-1]
        if self.direction == Directions.DOWN:
            y_head = y_head + 1
        elif self.direction == Directions.UP:
            y_head = y_head - 1
        elif self.direction == Directions.RIGHT:
            x_head = x_head + 1
        elif self.direction == Directions.LEFT:
            x_head = x_head - 1
        next_head = (x_head, y_head)

        # move the head
        self.body.append(next_head)

        # eventually eat the food
        can_eat = self.can_eat(food)
        if can_eat:
            self.eat()

        # advance the tail
        if self.length < len(self.body):
            self.body.pop(0)

        return can_eat

    def steer(self, direction):
        """Updates the direction if it is not the opposite of the current one."""
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
        return self.body[-1] == food.position

    def tail_collision(self):
        """Checks if the snake has has crashed against itself."""
        head = self.body[-1]
        for segment in self.body[:-1]:
            if head == segment:
                return True
        return False

    def bounds_collision(self, grid):
        """Checks if the snake has overcomed the grid bounds."""
        head = self.body[-1]
        if head not in grid.grid:
            return True
        return False

    def get_body(self):
        return copy.deepcopy(self.body)

    def fast_get_body(self):
        return self.body

    def dir_to_cell(self, cell):
        """Returns the direction to follow to reach cell."""
        head = self.body[-1]
        if cell[0] < head[0]:
            return Directions.LEFT
        elif cell[0] > head[0]:
            return Directions.RIGHT
        elif cell[1] < head[1]:
            return Directions.UP
        else:
            return Directions.DOWN