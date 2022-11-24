from player import Player
from directions import Directions

class BotS(Player):
    def delete_cell(self, grid, del_key):
        grid.pop(del_key, None)
        for key in grid:
            grid[key].pop(del_key, None)

    # restituisce la posizione della cella targhet rispetto alla cella head
    def graphDir_to_gameDir(self, head_pos, target_pos):

        if head_pos[0] < target_pos[0]:  # x shift
            return Directions.LEFT
        elif target_pos[0] > head_pos[0]:
            return Directions.RIGHT
        elif target_pos[1] < head_pos[1]:  # y shift
            return Directions.UP
        else:
            return Directions.DOWN

    def build_location(self, grid):
        locations = {}
        for key in grid:
            locations[key]=key
        return locations
