test_input = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''

import functools
import operator

def read_input(input):
    # return as dict with id: list of observations pairs
    games = {i+1:read_game_str(line.split(':')[1].strip()) for i, line in enumerate(input.strip().split('\n'))}
    return games

def read_game_str(s):
    # read line and convert to list of observations, with observation as dict with color: count
    observations = list(map(lambda x: list(map(lambda y: y.split(' '), x.split(', '))), s.split('; ')))
    return [{entry[1]: int(entry[0]) for entry in o} for o in observations]

def observe_games_max(games):
    # return the max number of observed dice per color as dict with id: observation, with observation as dict with color: max count
    result = {id:{color:max([observation[color] for observation in game if color in observation]) for color in ['red', 'green', 'blue']} for id, game in games.items()}
    return result

def observe_possible_games(games, max_allowed_counts):
    # return list of game IDs, filtered by which are possible, given restrictions passed in as max_allowed_counts
    result = [id for id, game in observe_games_max(games).items() if functools.reduce(lambda x, y: x and y, [game[color] <= max_allowed_counts[color] for color in game.keys()])]
    return result

def observe_power_of_games(games):
    # return list of power values for all games, with power being just the product of max observation values
    result = [functools.reduce(operator.mul, game.values()) for game in observe_games_max(games).values()]
    return result

def part1(input):
    games = read_input(input)
    result = sum(observe_possible_games(games, {'red': 12, 'green': 13, 'blue': 14}))
    print("Part 1: The sum of IDs of possible games is {}".format(result))

def part2(input):
    games = read_input(input)
    result = sum(observe_power_of_games(games))
    print("Part 2: The sum of the power of the minimal sets is {}".format(result))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)