test_input = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''

def get_instructions(moves):
    return [tuple(map(int, move.split(' ')[1::2])) for move in moves.strip().split('\n')]

def get_stack(configuration):
    rows = list(reversed(configuration.split('\n')))
    ncols = int(rows[0].split()[-1]) # assume we count up in order
    stacks = [[] for _ in range(ncols)]
    for row in rows[1:]:
        for col in range(ncols):
            beg = 4 * col + 1
            c = row[beg:beg+1]
            if c != ' ':
                stacks[col].append(c)
    return stacks

def read_input(input):
    cfg, moves = input.split('\n\n')
    return get_instructions(moves), get_stack(cfg)

def move_9000(stacks, count, mv_from, mv_to):
    for _ in range(count):
        stacks[mv_to].append(stacks[mv_from].pop())

def move_9001(stacks, count, mv_from, mv_to):
    tmp = stacks[mv_from][:-count]
    ex = stacks[mv_from][-count:]
    stacks[mv_to].extend(ex)
    stacks[mv_from] = tmp

def solve(input, move_fn):
    instructions, stacks = read_input(input)
    for ins in instructions:
        count, mv_from, mv_to = ins[0], ins[1] - 1, ins[2] -1
        move_fn(stacks, count, mv_from, mv_to)
    return ''.join([stack[-1] for stack in stacks])

def part1(input):
    answer = solve(input, move_9000)
    print("Part 1: {}".format(answer))

def part2(input):
    answer = solve(input, move_9001)
    print("Part 2: {}".format(answer))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)