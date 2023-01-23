from src.gui import snake_interface
from src.game import run_game

# get from the GUI the game settings
game_config = snake_interface()
# run the game
run_game(**game_config)