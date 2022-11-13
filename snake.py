from directions import Directions

class Snake:
    def __init__(self, color=(0, 190, 80), start_location="top-left"):
        self.color = color
        self.start_location = start_location

    def respawn(self, grid):
        self.length = 3
        if self.start_location == "top-left":
            self.body = ["(3,2)",
                         "(3,3)",
                         "(3,4)"]
            self.direction = Directions.DOWN
        if self.start_location == "bottom-right":
            self.body = ["(%d,%d)" % ((grid.x_blocks-4), (grid.y_blocks-4)),
                         "(%d,%d)" % ((grid.x_blocks-4),
                                      (grid.y_blocks-5)),
                         "(%d,%d)" % ((grid.x_blocks-4), (grid.y_blocks-6))]
            self.direction = Directions.UP

    def coordinate_from_nodes(self, node_list, grid):
        chars = ['(', ')']
        body_coord = []
        for node in node_list:
            node = node.translate(str.maketrans({ord(char): '' for char in chars}))
            node = node.split(',')
            for i in range(2):
                node[i] = int(node[i])
            body_coord[len(body_coord):] = [( int(node[0])*grid.block_size, int(node[1])*grid.block_size )]
        return body_coord

    def integer_from_string(self, node):
        chars = ['(', ')']
        node = node.translate(str.maketrans({ord(char): '' for char in chars}))
        node = node.split(',')
        for i in range(2):
            node[i] = int(node[i])
        return [int(node[0]), int(node[1])]

    def draw(self, game, window, grid):
        body_coord = self.coordinate_from_nodes(self.body, grid)
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

    def move(self, direction):
        self.__steer(direction)
        curr_head = self.body[-1]
        [x, y] = self.integer_from_string(curr_head)

        if self.direction == Directions.DOWN:
            y = y + 1
        elif self.direction == Directions.UP:
            y = y - 1
        elif self.direction == Directions.RIGHT:
            x = x + 1
        elif self.direction == Directions.LEFT:
            x = x - 1

        next_head = "(%d,%d)" % (x, y)
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
        return head == food.position[0]  # confronto tra nodi

    def check_tail_collision(self):
        head = self.body[-1]
        for i in range(len(self.body) - 1):
            segment = self.body[i]
            if head == segment:
                return True
        return False

    def check_adversarial_collision(self, adversarial_body):
        head = self.body[-1]
        for i in range(len(adversarial_body)):
            segment = adversarial_body[i]
            if head == segment:
                return True
        return False

    def check_bounds(self, grid):
        head = self.body[-1]
        if head not in grid.grid:
            return True
        return False
