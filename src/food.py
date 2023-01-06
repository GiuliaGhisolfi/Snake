import random as rand

class Food:
    def __init__(self, color):
        self.color = color
        self.position = None

    def draw(self, game, window, grid):
        """draw food"""
        [x, y] = self.coord_from_graph(grid)
        radious = (grid.block_size / 2) - 3
        game.draw.circle(
            window, self.color, (x + radious + 3, y + radious + 3), radious)

    def coord_from_graph(self, grid):
        """returns the coordinates on the window in pixels given the node in the graph"""
        node = self.position
        return (node[0]*grid.block_size, node[1]*grid.block_size)

    def is_overlapped(self, position, snake, grid):
        """returns true if the food position is on the snake or on an obstacle"""

        for segment in snake.get_body():
            if segment == position:
                return True
        for p in grid.get_obstacles():
            obstacle = (p.x_position, p.y_position)
            if position == obstacle:
                return True
        return False

    def respawn(self, snake, grid):
        """generete new food position s.t. it is inside the game grid, not overlapping the snake or obstacles"""
        def distance(n1, n2):
            return abs(n1[0]-n2[0]) + abs(n1[0] - n2[0])

        nodes = list(grid.grid.keys())
        rand.shuffle(nodes)  # random reorganize the order of the nodes

        possible_position = []
        for n in nodes:
            skip = False
            if distance(n, snake.get_body()[1]) <= 1:
                skip = True
                possible_position.append(n)
            if n != self.position and not self.is_overlapped(n, snake, grid):
                self.position = n
                return

        rand.shuffle(possible_position)
        self.position = possible_position[0]
