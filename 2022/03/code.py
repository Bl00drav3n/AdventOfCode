from functools import reduce

test_input = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''

def priority(c):
    return ord(c) - ord('a') + 1 if ord(c) >= ord('a') else ord(c) - ord('A') + 27

def group3(lst):
    for i in range(0, len(lst), 3):
        yield lst[i:i+3]

def part1(input):
    suckracks = [[list(map(priority, line[:len(line)//2])), list(map(priority, line[len(line)//2:]))] for line in input.strip().split('\n')]
    s = sum(map(lambda r: list(filter(lambda item: item in r[1], r[0]))[0], suckracks))
    print("Part 1: {}".format(s))

def part2(input):
    groups = list(group3(input.strip().split('\n')))
    s = sum(map(priority, [[i2 for i2 in set([i1 for i1 in group[0] if i1 in group[1]]) if i2 in group[2]][0] for group in groups]))
    print("Part 2: {}".format(s))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)