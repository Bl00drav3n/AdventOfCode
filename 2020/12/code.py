test_input = '''F10
N3
F7
R90
F11'''

EAST = 0
NORTH = 1
WEST = 2
SOUTH = 3

dir_mapping = {'E': EAST, 'N': NORTH, 'W': WEST, 'S': SOUTH}

def move_ship1(state, direction, value):
    if direction == NORTH:
        state['y'] += value
    if direction == SOUTH:
        state['y'] -= value
    if direction == WEST:
        state['x'] -= value
    if direction == EAST:
        state['x'] += value

def apply_instruction1(state, ins):
    direction = ins[0]
    value = int(ins[1:])
    if direction == 'F':
        move_ship1(state, state['facing'], value)
    elif direction == 'L':
        state['facing'] = (state['facing'] + (value // 90)) % 4
    elif direction == 'R':
        state['facing'] = (4 + state['facing'] - (value // 90)) % 4
    elif direction in ('E', 'N', 'W', 'S'):
        move_ship1(state, dir_mapping[direction], value)
    else:
        print('Invalid instruction', ins)

def move_ship2(state, value):
    state['x'] += value * state['wx']
    state['y'] += value * state['wy']

def move_waypoint(state, direction, value):
    if direction == 'N':
        state['wy'] += value
    if direction == 'S':
        state['wy'] -= value
    if direction == 'W':
        state['wx'] -= value
    if direction == 'E':
        state['wx'] += value

def rotate_left(state):
    wx, wy = state['wx'], state['wy']
    state['wx'] = -wy
    state['wy'] = wx

def rotate_right(state):
    wx, wy = state['wx'], state['wy']
    state['wx'] = wy
    state['wy'] = -wx

def apply_instruction2(state, ins):
    direction = ins[0]
    value = int(ins[1:])
    if direction == 'F':
        move_ship2(state, value)
    elif direction == 'L':
        [rotate_left(state) for i in range(value // 90)]
    elif direction == 'R':
        [rotate_right(state) for i in range(value // 90)]
    elif direction in ('E', 'N', 'W', 'S'):
        move_waypoint(state, direction, value)
    else:
        print('Invalid instruction', ins)
    
def get_manhattan_distance(state):
    return abs(state['x']) + abs(state['y'])

def create_ship(wx, wy):
    return {'x': 0, 'y': 0, 'wx': wx, 'wy': wy, 'facing': EAST}

def find_manhattan_distance1(input):
    ship = create_ship(0, 0)
    [apply_instruction1(ship, ins) for ins in input.splitlines()]
    return get_manhattan_distance(ship)

def find_manhattan_distance2(input):
    ship = create_ship(10, 1)
    [apply_instruction2(ship, ins) for ins in input.splitlines()]
    return get_manhattan_distance(ship)

print('Manhattan distance between destination and starting location part1 (TEST):', find_manhattan_distance1(test_input))
print('Manhattan distance between destination and starting location part2 (TEST):', find_manhattan_distance2(test_input))
with open('input.txt') as file:
    input = file.read()
    print('Manhattan distance between destination and starting location part1:', find_manhattan_distance1(input))
    print('Manhattan distance between destination and starting location part2:', find_manhattan_distance2(input))