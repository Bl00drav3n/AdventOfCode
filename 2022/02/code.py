test_input = '''A Y
B X
C Z
'''

def part1(input):
    score = {
        'A X': 4,
        'A Y': 8,
        'A Z': 3,
        'B X': 1,
        'B Y': 5,
        'B Z': 9,
        'C X': 7,
        'C Y': 2,
        'C Z': 6
    }
    scores = [score[line] for line in input.strip().split('\n')]
    print("Part 1: {}".format(sum(scores)))

def part2(input):
    score = {
        'B X': 1 + 0, # 1
        'C X': 2 + 0, # 2
        'A X': 3 + 0, # 3
        'A Y': 1 + 3, # 4
        'B Y': 2 + 3, # 5
        'C Y': 3 + 3, # 6
        'C Z': 1 + 6, # 7
        'A Z': 2 + 6, # 8
        'B Z': 3 + 6, # 9
    }
    scores = [score[line] for line in input.strip().split('\n')]
    print("Part 2: {}".format(sum(scores)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)