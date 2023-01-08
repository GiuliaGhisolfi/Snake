import numpy as np
import src.gui as gui
from src.game import run_game

gui.snake_interface()

config = None
log_file = './log.json'
if gui.player_info['type']=='greedy':
    config = './greedy.config'
if gui.player_info['type']=='hamilton':
    config = './hamilton.config'

game_config = {
    'grid_size': gui.SIZE,
    'grid_width': gui.X_BLOCKS,
    'grid_height': gui.Y_BLOCKS,
    'frame_delay': gui.FRAME_DELAY,
    'obstacles': gui.OBSTACLES,
    'autostart': gui.AUTOSTART,
    'max_executions': np.inf,
    'player_info': gui.player_info,
    'bot_config': config,
    'log_file': log_file,
    'test_mode': False,
}

run_game(**game_config)