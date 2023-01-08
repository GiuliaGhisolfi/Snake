from src.game import run_game
import src.colors as colors
from src.config_parsing import *

# greedy bot configuration and log files paths
greedy_configs_fold = './test/greedy_configs/'
greedy_configs = [
    greedy_configs_fold+'bot1.config',
    greedy_configs_fold+'bot2.config',
    greedy_configs_fold+'bot3.config',
    greedy_configs_fold+'bot4.config',
    greedy_configs_fold+'bot5.config',
    greedy_configs_fold+'bot6.config',
    greedy_configs_fold+'bot7.config',
    greedy_configs_fold+'bot8.config',
    greedy_configs_fold+'bot9.config',
    greedy_configs_fold+'bot10.config'
]
greedy_results_fold = './test/greedy_results/'
greedy_logs = [
    greedy_results_fold+'log1.json',
    greedy_results_fold+'log2.json',
    greedy_results_fold+'log3.json',
    greedy_results_fold+'log4.json',
    greedy_results_fold+'log5.json',
    greedy_results_fold+'log6.json',
    greedy_results_fold+'log7.json'  # ,
    # greedy_results_fold+'log8.json',
    # greedy_results_fold+'log9.json',
    # greedy_results_fold+'log10.json'
]

# hamilton bot configuration and log files paths
hamilton_configs_fold = './test/hamilton_configs/'
hamilton_configs = [
    hamilton_configs_fold+'bot1.config',
    hamilton_configs_fold+'bot2.config',
    hamilton_configs_fold+'bot3.config',
    hamilton_configs_fold+'bot4.config',
    hamilton_configs_fold+'bot5.config',
    hamilton_configs_fold+'bot6.config',
    hamilton_configs_fold+'bot7.config',
    hamilton_configs_fold+'bot8.config',
    hamilton_configs_fold+'bot9.config',
    hamilton_configs_fold+'bot10.config',
    hamilton_configs_fold+'bot11.config'
]
hamilton_results_fold = './test/hamilton_results/'
ham_logs = [
    hamilton_results_fold+'log1.json',
    hamilton_results_fold+'log2.json',
    hamilton_results_fold+'log3.json',
    hamilton_results_fold+'log4.json',
    hamilton_results_fold+'log5.json',
    hamilton_results_fold+'log6.json',
    hamilton_results_fold+'log7.json',
    hamilton_results_fold+'log8.json',
    hamilton_results_fold+'log9.json',
    hamilton_results_fold+'log10.json',
    hamilton_results_fold+'log11.json'
]

# test greedy bot

"""print('------ Bot greedy ------')
for i, log_file in enumerate(greedy_logs):
    print('config = ' + str(i + 1))
    player_info = {'color': colors.GREEN, 'start_location': 'top-left'}
    player_info['type'] = 'greedy'
    game_config = get_game_config(greedy_configs_fold + 'game_' + str(i + 1) + '.config')
    game_config['player_info'] = player_info
    game_config['bot_config'] = greedy_configs_fold + 'bot7.config'
    game_config['log_file'] = log_file
    game_config['test_mode'] = True
    run_game(**game_config)"""

# test hamilton bot

print('------ Bot hamilton ------')
for config_file, log_file in zip(hamilton_configs, ham_logs):
    print('config = %s'%config_file)
    player_info = {'color': colors.GREEN, 'start_location': 'top-left'}
    player_info['type'] = 'hamilton'
    game_config = get_game_config(hamilton_configs_fold+'game.config')
    game_config['player_info'] = player_info
    game_config['bot_config'] = config_file
    game_config['log_file'] = log_file
    game_config['test_mode'] = True
    run_game(**game_config)