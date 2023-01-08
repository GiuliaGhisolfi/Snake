import numpy as np
import src.gui as gui
from src.game import start

gui.snake_interface()

config = None
log_file = './log.json'
if gui.player_info['type']=='greedy':
    config = './greedy.config'
if gui.player_info['type']=='hamilton':
    config = './hamilton.config'

start_params = {
    'size': gui.SIZE,
    'x_blocks': gui.X_BLOCKS,
    'y_blocks': gui.Y_BLOCKS,
    'frame_delay': gui.FRAME_DELAY,
    'obstacles': gui.OBSTACLES,
    'autostart': gui.AUTOSTART,
    'max_executions': np.inf,
    'player_info': gui.player_info,
    'bot_config': config,
    'log_file': log_file,
    'test_mode': False,
}

start(**start_params)