test_input = '''
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
'''

import time

def read_input(input):
    locks = []
    keys = []
    for schematic in input.strip().split('\n\n'):
        heights = [0] * 5 
        rows = schematic.split('\n')
        if schematic[0] == '#':
            locks.append(heights)
        else:
            keys.append(heights)
            rows = list(reversed(rows))
        for row in rows[1:]:
            for i in range(5):
                if row[i] == '#':
                    heights[i] += 1
    return {'keys': keys, 'locks': locks }

def print_time_diff(start, end):
    print("Time: {:.3f} sec".format((end - start)/1e9))

def part1(input):
    start = time.time_ns()
    data = read_input(input)
    pairs = []
    for key in data['keys']:
        for lock in data['locks']:
            if max([key[column] + lock[column] for column in range(5)]) <= 5:
                # no overlap
                pairs.append((key, lock))
    end = time.time_ns()
    
    print("Part 1: There are {} unique key/lock pairs that fit together without overlapping." .format(len(pairs)))
    print_time_diff(start, end)

def part2(input):
    start = time.time_ns()
    end = time.time_ns()
    print("Part 2: " .format())
    print_time_diff(start, end)

print('---TEST---')
part1(test_input)

with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)
