import random as rand

class Food:
    def __init__(self, color):
        self.color = color
        self.position = None

    def draw(self, game, window, grid):
        [x,y] = self.coord_from_graph(grid)
        radious = (grid.block_size / 2) - 3
        game.draw.circle(
            window, self.color, (x + radious + 3, y + radious + 3), radious)
        
    def coord_from_graph(self, grid):
        node = self.position
        return (node[0]*grid.block_size, node[1]*grid.block_size)

    def is_overlapped(self, position, snakes, grid):
        for s in snakes:
            for segment in s.get_body():
                if segment == position:
                    return True
        for p in grid.get_obstacles():
            obstacle = (p.x_position, p.y_position)
            if position == obstacle:
                return True
        return False

    def respawn(self, snakes, grid):
        def distance(n1, n2):
            return abs(n1[0]-n2[0]) + abs(n1[0] - n2[0])

        nodes = list(grid.grid.keys())
        rand.shuffle(nodes)
        
        scartati = []
        for n in nodes:
            skip = False
            for s in snakes:
                if distance(n, s.get_body()[1]) <= 1:
                    skip = True
                    scartati.append(n)
            if n != self.position and not self.is_overlapped(n, snakes, grid):
                self.position = n
                return

        rand.shuffle(scartati)
        self.position = scartati[0]