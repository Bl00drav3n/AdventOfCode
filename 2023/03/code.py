test_input = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''

import re

def point_in_rect(p, upper_left, lower_right):
    # Test if point p as 2-tuple is inside the rectangle defined by the 2-tuples upper_left and lower_right
    return p[0] >= upper_left[0] and p[0] <= lower_right[0] and p[1] >= upper_left[1] and p[1] <= lower_right[1]

def is_part_number(n, symbols):
    # Test if number n is adjacent to any symbol
    upper_left = (n[0][0]-1, n[0][1]-1)
    lower_right = (n[1][0]+1, n[1][1]+1)
    for s in symbols:
        if point_in_rect(s[0], upper_left, lower_right):
            return True
    return False

def get_parts(numbers, symbols):
    # Return list of all numbers that are part numbers
    return [n for n in numbers if is_part_number(n, symbols)]

def get_adjacent_part_numbers(s, part_numbers):
    # Return list of values of part numbers which are adjacent to given symbol s
    return [int(n[2]) for n in part_numbers if point_in_rect(s[0], (n[0][0]-1, n[0][1]-1), (n[1][0]+1, n[1][1]+1))]

def parse(input):
    # Return list of numbers and symbols as tuples ((line,left),(line,right),name)
    lines = input.strip().split('\n')
    numbers_pattern = re.compile(r'\d+')
    symbols_pattern = re.compile(r'[^\w.]')
    numbers = []
    symbols = []
    for i, line in enumerate(lines):
        numbers += [((i, m.span()[0]), (i, m.span()[1]-1), m.group()) for m in numbers_pattern.finditer(line)]
        symbols += [((i, m.span()[0]), (i, m.span()[1]-1), m.group()) for m in symbols_pattern.finditer(line)]
    return numbers, symbols

def part1(input):
    numbers, symbols = parse(input)
    part_numbers = [int(p[2]) for p in get_parts(numbers, symbols)]
    print("Part 1: The sum of all the part numbers is {}".format(sum(part_numbers)))

def part2(input):
    numbers, symbols = parse(input)
    parts = get_parts(numbers, symbols)
    gear_ratios = [p[0]*p[1] for p in [get_adjacent_part_numbers(s, parts) for s in symbols if s[2] == '*'] if len(p) == 2]
    print("Part 2: The sum of all the gear ratios is {}".format(sum(gear_ratios)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)