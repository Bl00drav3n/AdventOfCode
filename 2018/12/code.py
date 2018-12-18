# rules are encoded as 5bit indices: ..#.. = 4, ##### = 31, etc.

test_initial_state = "#..#.#..##......###...###"
test_rules = [
#   0  1  2  3  4  5  6  7
    0, 0, 0, 1, 1, 0, 0, 0, # 0
    1, 0, 1, 1, 1, 0, 0, 1, # 1
    0, 0, 0, 0, 0, 1, 0, 1, # 2
    0, 0, 1, 1, 1, 1, 1, 0  # 3
]

initial_state = ".##..##..####..#.#.#.###....#...#..#.#.#..#...#....##.#.#.#.#.#..######.##....##.###....##..#.####.#"
rules = [
#   0  1  2  3  4  5  6  7
    0, 0, 0, 1, 0, 0, 0, 1, # 0
    1, 1, 1, 1, 1, 0, 0, 1, # 1
    0, 0, 0, 1, 1, 1, 0, 0, # 2
    1, 0, 1, 0, 1, 1, 0, 0  # 3
]

#BLA
initial_state = ".##..##..####..#.#.#.###....#...#..#.#.#..#...#....##.#.#.#.#.#..######.##....##.###....##..#.####.#"
rules = [
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    1,
    1,
    0,
    0,
    1,
    0,
    0,
    0,
    1,
    1,
    1,
    0,
    0,
    1,
    0,
    1,
    0,
    1,
    1,
    0,
    0
]

def set_debug():
    global initial_state
    global rules
    global test_initial_state
    global test_rules
    initial_state = test_initial_state
    rules = test_rules

from functools import reduce
def bits_to_int(bits):
    return reduce(lambda x, y: (x << 1) + y, bits)

def pattern_to_bits(pattern):
    return map(lambda x: 1 if x == '#' else 0, pattern)

def pattern_to_int(pattern):
    return bits_to_int(pattern_to_bits(pattern))

def state_to_bits(state):
    return map(lambda x: 1 if x & 4 else 0, state)

def state_to_pattern(state):
    return map(lambda x: '#' if x else '.', state_to_bits(state))

def convert_to_string(state):
    return "".join(state_to_pattern(state))

def update(state, rules, offset):
    state = [0, 0, 0, 0, 0] + state + [0, 0, 0, 0, 0]
    new_state = []
    for i in range(2, len(state) - 2):
        new_state.append(bits_to_int(map(lambda x: rules[x], state[i - 2: i + 3])))
    return new_state, offset - 3

def run(tries, out):
    global initial_state
    global rules
    initial_state = ".." + initial_state + ".."
    state = []
    for i in range(2, len(initial_state) - 2):
        pattern = initial_state[i - 2 : i + 3]
        state.append(pattern_to_int(pattern))

    out.write(''.join(['.'] * (3 * tries)) + convert_to_string(state) + '\n')
    offset = 0
    last = 0
    for i in range(0, tries):
        new_state, offset = update(state, rules, offset)
        out.write(''.join(['.'] * (3 * (tries - i - 1))) + convert_to_string(new_state) + '\n')
        if new_state[4:-2] == state:
            pass
            #print('transformation is simply translation, terminating at ' + str(i))
            #break
        state = new_state
        s = sum(map(lambda x, y: (x + offset) * y, range(0, len(state)), state_to_bits(state)))
        print(i, s, s - last)
        last = s

    return state, offset, i

import sys
with open('out.txt', 'w') as f:
    #set_debug()
    state, offset, n = run(tries=200, out=f)