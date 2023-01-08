import random as rand

class Food:
    """This class implements the food."""

    def __init__(self, color):
        self.color = color
        self.position = None

    def draw(self, game, window, grid):
        """Draw the food."""
        [x, y] = self.coord_from_graph(grid)
        radius = (grid.block_size / 2) - 3
        game.draw.circle(
            window, self.color, (x + radius + 3, y + radius + 3), radius
        )

    def coord_from_graph(self, grid):
        """Returns the pixel coordinates of the food given the position on the grid."""
        return (self.position[0]*grid.block_size, self.position[1]*grid.block_size)

    def is_overlapped(self, position, snake, grid):
        """Returns true if the food overlaps the snake's body or an obstacle."""
        for segment in snake.get_body():
            if segment == position:
                return True
        for obstacle in grid.get_obstacles():
            if (obstacle.x_position, obstacle.y_position) == position:
                return True
        return False

    def respawn(self, snake, grid):
        """Randomly generates a new food position, avoiding (if possible) 
        the cells adjacent to the snake's head."""
        def distance(n1, n2):
            return abs(n1[0]-n2[0]) + abs(n1[0] - n2[0]) # REVIEW: aima_utils manhattan distance?

        nodes = list(grid.grid.keys())
        rand.shuffle(nodes)

        possible_positions = [] # REVIEW: why a list?
        for n in nodes:
            if distance(n, snake.get_body()[1]) <= 1:
                possible_positions.append(n)
            if n != self.position and not self.is_overlapped(n, snake, grid):
                self.position = n
                return

        rand.shuffle(possible_positions) # REVIEW: needed?
        self.position = possible_positions[0]