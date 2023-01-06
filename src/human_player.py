import pygame
from src.directions import Directions
from src.player import Player

class HumanPlayer(Player):
    def __init__(
        self, 
        game, 
        up_key=pygame.K_UP, 
        down_key=pygame.K_DOWN, 
        right_key=pygame.K_RIGHT, 
        left_key=pygame.K_LEFT):

        self.game = game
        self.up_key = up_key
        self.down_key = down_key
        self.right_key = right_key
        self.left_key = left_key

    def get_next_move(self):
        keys = self.game.key.get_pressed()
        dir = None
        if keys[self.up_key]:
            dir = Directions.UP
        elif keys[self.down_key]:
            dir = Directions.DOWN
        elif keys[self.right_key]:
            dir = Directions.RIGHT
        elif keys[self.left_key]:
            dir = Directions.LEFT
        return dir
    
    def set_restart_game(self):
        pass