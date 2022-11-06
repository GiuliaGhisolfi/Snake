import threading
import random
from directions import Directions
from player import Player

class Bot(Player):
    def __init__(self):
        self.next_move = None
        self.lock = threading.Lock()

    def compute_next_move(self, snakes, my_index, food, chessboard):
        # move = Directions(random.randint(0, 3))
        if len(snakes) > 1:
            adv_index = 1 if my_index == 0 else 0
            move = self.binary_search(snakes[my_index], snakes[adv_index], food, chessboard)
        else: # per adesso se non c'è un avversario si muove in modo casuale
            move = Directions(random.randint(0, 3))
        self.lock.acquire()
        self.next_move = move
        self.lock.release()

    def get_next_move(self):
        self.lock.acquire()
        move = self.next_move
        self.lock.release()
        return move


    def binary_search(self, my_snake, adversary_snake, food, chessboard):
        self.my_position = my_snake.body[-1]
        self.my_body = my_snake.body
        self.adversary_position = adversary_snake.body[-1]
        self.adversary_body = adversary_snake.body
        self.food_position = (food.x, food.y)
        self.block_size = chessboard.block_size
        self.x_matrix = chessboard.x_blocks
        self.y_matrix = chessboard.y_blocks
        self.adversary_direction = adversary_snake.direction
        self.next_adversary_position()

        # TODO: bisognerebbe mettere i controlli affinché se non posso muovermi 
        # in una direzione ottima, mi muovo in una consentita
        if self.my_position[0] > self.food_position[0]:
            if self.left_allowed():
                return Directions.LEFT

        if self.my_position[0] < self.food_position[0]:
            if self.right_allowed():
                return Directions.RIGHT

        if self.my_position[1] > self.food_position[1]:
            if self.up_allowed():
                return Directions.UP

        if self.my_position[1] < self.food_position[1]:
            if self.down_allowed():
                return Directions.DOWN
        # line 43 -> 57 ho provato a mettere questi controlli ma mi sembra che funzioni peggio
        """if self.my_position[0] > self.food_position[0]:
            self.possible_move_left = self.left_allowed()
            if self.possible_move_left:
                return Directions.LEFT
            else:
                self.possible_move_right = self.right_allowed

        if self.my_position[0] < self.food_position[0]:
            self.possible_move_right = self.right_allowed           
            if self.possible_move_right:
                return Directions.RIGHT
            else:
                self.possible_move_left = self.left_allowed()

        if self.my_position[1] > self.food_position[1]:
            self.possible_move_up = self.up_allowed 
            if self.possible_move_up:
                return Directions.UP
            else:
                self.possible_move_down = self.down_allowed 

        if self.my_position[1] < self.food_position[1]:
            self.possible_move_down = self.down_allowed 
            if self.possible_move_down:
                return Directions.DOWN
            else:
                self.possible_move_up = self.up_allowed 
        
        # se non posso muovermi in una direzione ottimale mi muovo in una direzione in cui non muoio se possibile
        if self.my_position[0] == self.food_position[0]:
            self.possible_move_left = self.left_allowed()
        if self.possible_move_left:
            return Directions.LEFT
        
        if self.my_position[0] == self.food_position[0]:
            self.possible_move_right = self.right_allowed
        if self.possible_move_right:
            return Directions.RIGHT
        
        if self.my_position[1] == self.food_position[1]:
            self.possible_move_up = self.up_allowed 
        if self.possible_move_up:
            return Directions.UP
        
        if self.my_position[1] == self.food_position[1]:
            self.possible_move_down = self.down_allowed 
        if self.possible_move_down:
            return Directions.DOWN
"""


    def left_allowed(self):
        check = 1
        for segment in self.next_position_adversary:
            if (self.my_position[0] - self.block_size, self.my_position[1]) == segment:
                check = 0
        for segment in self.my_body:
            if (self.my_position[0] - self.block_size, self.my_position[1]) == segment:
                check = 0
        if self.my_position[0] - self.block_size < 0:
            check = 0
        return check


    def right_allowed(self):
        check = 1
        for segment in self.next_position_adversary:
            if (self.my_position[0] + self.block_size, self.my_position[1]) == segment:
                check = 0
        for segment in self.my_body:
            if (self.my_position[0] + self.block_size, self.my_position[1]) == segment:
                check = 0
        if self.my_position[0] + self.block_size > (self.x_matrix - 1) *self.block_size:
            check = 0
        return check


    def up_allowed(self):
        check = 1
        for segment in self.next_position_adversary:
            if (self.my_position[0], self.my_position[1] - self.block_size) == segment:
                check = 0
        for segment in self.my_body:
            if (self.my_position[0], self.my_position[1] - self.block_size) == segment:
                check = 0
        if self.my_position[1] - self.block_size < 0:
            check = 0
        return check


    def down_allowed(self):
        check = 1
        for segment in self.next_position_adversary:
            if (self.my_position[0], self.my_position[1] + self.block_size) == segment:
                check = 0
        for segment in self.my_body:
            if (self.my_position[0], self.my_position[1] + self.block_size) == segment:
                check = 0
        if self.my_position[1] + self.block_size > (self.y_matrix - 1) *self.block_size:
            check = 0
        return check


    def next_adversary_position(self):
        self.next_position_adversary = self.adversary_body[1:]
        
        if (self.adversary_position[0] + self.block_size, self.adversary_position[1]) not in self.next_position_adversary:
            if self.adversary_direction != Directions.LEFT or \
                self.adversary_position[0] + self.block_size > (self.x_matrix - 1) *self.block_size:
                        self.next_position_adversary.append(
                            (self.adversary_position[0] + self.block_size, self.adversary_position[1]))
        
        if (self.adversary_position[0] - self.block_size, self.adversary_position[1]) not in self.next_position_adversary:  
            if self.adversary_direction != Directions.RIGHT or \
                self.adversary_position[0] - self.block_size < 0:
                    self.next_position_adversary.append(
                        (self.adversary_position[0] - self.block_size, self.adversary_position[1]))
        
        if (self.adversary_position[0], self.adversary_position[1] + self.block_size) not in self.next_position_adversary:     
            if self.adversary_direction != Directions.UP or \
                self.adversary_position[1] + self.block_size > (self.y_matrix - 1) *self.block_size:
                    self.next_position_adversary.append(
                        (self.adversary_position[0], self.adversary_position[1] + self.block_size))
        
        if (self.adversary_position[0], self.adversary_position[1] - self.block_size) not in self.next_position_adversary:    
            if self.adversary_direction != Directions.DOWN or \
                self.adversary_position[1] - self.block_size < 0:
                    self.next_position_adversary.append(
                        (self.adversary_position[0], self.adversary_position[1] - self.block_size))