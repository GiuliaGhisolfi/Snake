from src.game import run_game
from src.config_parsing import *

greedy_configs_fold = './test/greedy_configs/'
greedy_results_fold = './test/greedy_results/'

# list of greedy configurations to test
greedy_configs = [
    greedy_configs_fold+'bot1.config'
]
# list of game configurations to test
greedy_games = [
    greedy_configs_fold+'game1.config'
]
# list of log file paths to save greedy test results
greedy_logs = [
    greedy_results_fold+'log1.json'
]

hamilton_configs_fold = './test/hamilton_configs/'
hamilton_results_fold = './test/hamilton_results/'

# list of hamilton configurations to test
hamilton_configs = [
    hamilton_configs_fold+'bot1.config'
]
# list of game configurations to test
hamilton_games = [
    hamilton_configs_fold+'game1.config'
]
# list of log file paths to save hamilton test results
hamilton_logs = [
    hamilton_results_fold+'log1.json'
]

# test greedy bot
print('------ Bot greedy ------')
for i in range(len(greedy_logs)):
    print('test ' + str(i + 1))
    game_config = get_game_config(greedy_games[i])
    game_config['player_info'] = 'greedy'
    game_config['bot_config'] = greedy_configs[i]
    game_config['log_file'] = greedy_logs[i]
    game_config['test_mode'] = True
    run_game(**game_config)

# test hamilton bot

print('------ Bot hamilton ------')
for i in range(len(hamilton_logs)):
    print('test ' + str(i + 1))
    game_config = get_game_config(hamilton_games[i])
    game_config['player_info'] = 'hamilton'
    game_config['bot_config'] = hamilton_configs[i]
    game_config['log_file'] = hamilton_logs[i]
    game_config['test_mode'] = True
    run_game(**game_config)
