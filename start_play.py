import numpy as np
import src.gui as gui
from src.game import start

greedy_configs_fold = './test/greedy_configs/'
hamilton_configs_fold = './test/hamilton_configs/'

gui.snake_interface()

config = None
log_file = None
if gui.player_info['type']=='greedy':
    config = greedy_configs_fold+'bot7.config'
    log_file = greedy_configs_fold+'log1.json'
if gui.player_info['type']=='hamilton':
    config = hamilton_configs_fold+'bot4.config'
    log_file = hamilton_configs_fold+'log6.json'

start_params = {
    'size': gui.SIZE,
    'x_blocks': gui.X_BLOCKS,
    'y_blocks': gui.Y_BLOCKS,
    'frame_delay': gui.FRAME_DELAY,
    'obstacles': gui.OBSTACLES,
    'autostart': gui.AUTOSTART,
    'executions': np.inf,
    'player_info': gui.player_info,
    'bot_config': config,
    'log_file': log_file,
    'test_mode': False,
}

start(start_params)