import src.gui as gui
from src.game import run_game

game_config = gui.snake_interface()
run_game(**game_config)