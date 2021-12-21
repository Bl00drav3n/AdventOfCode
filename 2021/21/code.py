import time
test_input = '''Player 1 starting position: 4
Player 2 starting position: 8'''

def dirac_dice(state):
    state[0] = (state[0] % 100) + 1
    return state[0]

def part1(input):
    players = [int(line.split(':')[1].strip()) for line in input.strip().split('\n')]
    t0 = time.time_ns()
    scores = [0, 0]
    player = 0
    dice = [0]
    n = 0
    while scores[1 - player] < 1000:
        d1 = dirac_dice(dice)
        d2 = dirac_dice(dice)
        d3 = dirac_dice(dice)
        players[player] = ((players[player] + d1 + d2 + d3 - 1) % 10) + 1
        scores[player] += players[player]
        #print('Player {} rolls {}+{}+{} and moves to space {} for a total score of {}.'.format(player + 1, d1, d2, d3, players[player], scores[player]))
        player = 1 - player
        n += 3
    loser = player
    print("Part 1: The losing player had {} points and the die had been rolled a total of {} times; {} * {} = {}".format(scores[loser], n, scores[loser], n, scores[loser] * n))

def part2(input):
    # TODO(rav3n): Throw math at it
    print("Part 2:".format())

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)