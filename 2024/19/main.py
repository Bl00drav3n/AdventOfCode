test_input = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''

def check(design, patterns):
    # table at position i holds information about whether the substring 0:i
    # can be split into segments contained in the list of patterns. Table entry 0 corresponds
    # to a 0-length substring, we set it to True so the algorithm can start once it finds the first
    # valid pattern at the start of the input.
    # At each position j we iterate over all substrings i:j. If the substring
    # is a valid pattern and table[i] is True, then we know we can split the input
    # into segments for substring 0:i and also for substring i:j. This in turn means we can split the input 
    # for substring 0:j. Hence we set table[j] to True and continue.
    # If the last position in the table is True, then we found that it is possible
    # to split the input into segments of patterns, else it is not possible.
    table = [False] * (len(design) + 1)
    table[0] = True
    for j in range(1, len(design) + 1):
        for i in range(j):
            if table[i] and design[i:j] in patterns:
                table[j] = True
                break
    return table[len(design)]

def check_possiblities(design, patterns):
    # For every position of the input we record how many times we can
    # reach any other position by matching subsequences at the current position.
    # If we had n possible ways to reach position i, and we look at a matching subsequence
    # starting at position i that has a length m, then there are n possible ways to reach position i + m.
    # There is one possiblity to reach position 0, hence we initialize it with 1.
    # The last entry of the list will contain the number of possibilities to reach the end of the input,
    # given the allowed patterns.
    # Powered by https://github.com/Fractura/advent-of-code/blob/main/2024/19/Program.cs
    combinations = [0] * (len(design) + 1)
    combinations[0] = 1
    # We cache the length here to speed up the loop (runs 50% faster than previous version)
    patterns = [(p, len(p)) for p in patterns]
    for i in range(len(design)):
        for pattern, length in patterns:
            if design[i:i+length] == pattern:
                combinations[i + length] += combinations[i]
    return combinations[-1]

def timediff(start_ns, end_ns):
    return (end_ns - start_ns)/1e9

import time                
def part1(input):
    patterns, designs = input.strip().split('\n\n')
    patterns = patterns.split(', ')
    designs = designs.split('\n')
    start = time.time_ns()
    count = sum([1 for design in designs if check(design, patterns)])
    end = time.time_ns()
    print("Part 1: The number of possible designs is {}." .format(count))
    print("TIME: {:.3f} sec".format(timediff(start, end)))

def part2(input):
    patterns, designs = input.strip().split('\n\n')
    patterns = patterns.split(', ')
    designs = designs.split('\n')
    start = time.time_ns()
    total = sum([check_possiblities(design, patterns) for design in designs])
    end = time.time_ns()
    print("Part 2: The sum of the number of different ways you could make each design is {}.".format(total))
    print("TIME: {:.3f} sec".format(timediff(start, end)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)