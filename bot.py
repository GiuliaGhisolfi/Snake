import threading
import random
from directions import Directions
from player import Player

class Bot(Player):
    def __init__(self):
        self.next_move = None
        self.lock = threading.Lock()

    def compute_next_move(self):
        move = Directions(random.randint(0, 3))
        self.lock.acquire()
        self.next_move = move
        self.lock.release()

    def get_next_move(self):
        self.lock.acquire()
        move = self.next_move
        self.lock.release()
        return move