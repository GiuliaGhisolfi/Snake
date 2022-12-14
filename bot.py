from player import Player
from directions import Directions

class Bot(Player):

    # IRENE: da eliminare, così possiamo eliminare l'intera classe
    # restituisce la posizione della cella targhet rispetto alla cella head
    def graphDir_to_gameDir(self, head_pos, target_pos):
        if target_pos[0] < head_pos[0]:  # x shift
            return Directions.LEFT
        elif target_pos[0] > head_pos[0]:
            return Directions.RIGHT
        elif target_pos[1] < head_pos[1]:  # y shift
            return Directions.UP
        else:
            return Directions.DOWN