class Player():
    """This class implements a player of the game."""
    def __init__(self):
        self.restart_game = True

    def set_restart_game(self):
        self.restart_game = True
        
    def reset_restart_game(self):
        self.restart_game = False
    
    def get_next_move(self):
        return None
    
    def get_path_to_draw(self):
        return [[],[],[]]
    
    def write_log(self):
        return