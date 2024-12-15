test_input = '''
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''

SPACE = '.'
WALL = '#'
BOX = 'O'
ROBOT = '@'
WIDE_BOX_LEFT = '['
WIDE_BOX_RIGHT = ']'

UP = '^'
RIGHT = '>'
DOWN = 'v'
LEFT = '<'

def read_input(input):
    map_string, sequence = input.strip().split('\n\n')
    warehouse = [list(line) for line in map_string.strip().split('\n')]
    bounds = (len(warehouse[0]), len(warehouse))
    sequence = sequence.replace('\n', '')
    robot = get_robot(warehouse, bounds)
    warehouse[robot[1]][robot[0]] = SPACE
    return warehouse, bounds, robot, sequence

def read_input2(input):
    map_string, sequence = input.strip().split('\n\n')
    warehouse = []
    for line in map_string.strip().split('\n'):
        row = []
        warehouse.append(row)
        for item in line:
            if item == BOX:
                row.append(WIDE_BOX_LEFT)
                row.append(WIDE_BOX_RIGHT)
            elif item == WALL:
                row.append(WALL)
                row.append(WALL)
            elif item == ROBOT:
                row.append(ROBOT)
                row.append(SPACE)
            elif item == SPACE:
                row.append(SPACE)
                row.append(SPACE)
    bounds = (len(warehouse[0]), len(warehouse))
    robot = get_robot(warehouse, bounds)
    warehouse[robot[1]][robot[0]] = SPACE
    return warehouse, bounds, robot, sequence

def get_robot(warehouse, bounds):
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            p = (x, y)
            tile = warehouse[y][x]
            if tile == ROBOT:
                return p
    return None, None

def get_tiles_of_type(warehouse, bounds, type):
    tiles = set()
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            if warehouse[y][x] == type:
                tiles.add((x, y))
    return tiles

def get_move_direction(instruction):
    mx, my = 0, 0
    if instruction == UP: my = -1
    elif instruction == DOWN: my = 1
    elif instruction == RIGHT: mx = 1
    elif instruction == LEFT: mx = -1
    return mx, my

def try_move(warehouse, bounds, pos, move):
    result = pos
    x, y = pos[0], pos[1]
    px, py = x + move[0], y + move[1]
    tile = warehouse[py][px]
    if tile == BOX:
        try_move(warehouse, bounds, (px, py), move)
    if warehouse[py][px] == SPACE:
        warehouse[py][px] = warehouse[y][x]
        warehouse[y][x] = SPACE
        result = (px, py)
    return result

# This turned out to be a bit of a mess and would need some refactoring
# to be readable, but it works. It makes a difference whether we move horizontally
# or vertically, as horizontal moves can be easily done recursively.
# For the vertical direction, one has to check if all boxes
# can actually move at once. Doing it recursively meant splitting the algorithm into
# checking all boxes first, and then move all the boxes up/down at once.

def check_vmove_wbox(warehouse, bounds, left, right, instruction):
    assert instruction in (UP, DOWN), "Invalid instruction for vertical movement!"
    if instruction == UP:
        left_p = left[0], left[1] - 1
        right_p = right[0], right[1] - 1
    elif instruction == DOWN:
        left_p = left[0], left[1] + 1
        right_p = right[0], right[1] + 1

    left_tile = warehouse[left_p[1]][left_p[0]]
    right_tile = warehouse[right_p[1]][right_p[0]]
    left_allow = True
    right_allow = True
    if left_tile in (WIDE_BOX_LEFT, WIDE_BOX_RIGHT):
        next_left = left_p
        next_right = left_p[0] + 1, left_p[1]
        if left_tile == WIDE_BOX_RIGHT:
            next_left = left_p[0] - 1, left_p[1]
            next_right = left_p
        left_allow = check_vmove_wbox(warehouse, bounds, next_left, next_right, instruction)
    if right_tile in (WIDE_BOX_LEFT, WIDE_BOX_RIGHT):
        next_left = right_p
        next_right = right_p[0] + 1, right_p[1]
        if right_tile == WIDE_BOX_RIGHT:
            next_left = right_p[0] - 1, right_p[1]
            next_right = right_p
        right_allow = check_vmove_wbox(warehouse, bounds, next_left, next_right, instruction)
    return left_tile != WALL and right_tile != WALL and left_allow and right_allow

def try_move_wbox(warehouse, bounds, left, right, instruction):
    if instruction == LEFT:
        allow_move = True
        p = left[0] - 1, left[1]
        if warehouse[p[1]][p[0]] == WIDE_BOX_RIGHT:
            allow_move = try_move_wbox(warehouse, bounds, (p[0] - 1, p[1]), p, instruction)    
        if warehouse[p[1]][p[0]] == SPACE and allow_move:
            warehouse[p[1]][p[0]] = WIDE_BOX_LEFT
            warehouse[left[1]][left[0]] = WIDE_BOX_RIGHT
            warehouse[right[1]][right[0]] = SPACE
            return True
    elif instruction == RIGHT:
        allow_move = True
        p = right[0] + 1, right[1]
        if warehouse[p[1]][p[0]] == WIDE_BOX_LEFT:
            allow_move = try_move_wbox(warehouse, bounds, p, (p[0] + 1, p[1]), instruction)
        if warehouse[p[1]][p[0]] == SPACE and allow_move:
            warehouse[p[1]][p[0]] = WIDE_BOX_RIGHT
            warehouse[right[1]][right[0]] = WIDE_BOX_LEFT
            warehouse[left[1]][left[0]] = SPACE
            return True
    elif instruction in (UP, DOWN):
        if instruction == UP:
            left_p = left[0], left[1] - 1
            right_p = right[0], right[1] - 1
        elif instruction == DOWN:
            left_p = left[0], left[1] + 1
            right_p = right[0], right[1] + 1
        left_tile = warehouse[left_p[1]][left_p[0]]
        if left_tile in (WIDE_BOX_LEFT, WIDE_BOX_RIGHT):
            next_left = left_p
            next_right = left_p[0] + 1, left_p[1]
            if left_tile == WIDE_BOX_RIGHT:
                next_left = left_p[0] - 1, left_p[1]
                next_right = left_p
            try_move_wbox(warehouse, bounds, next_left, next_right, instruction)
        right_tile = warehouse[right_p[1]][right_p[0]]
        if right_tile in (WIDE_BOX_LEFT, WIDE_BOX_RIGHT):
            next_left = right_p
            next_right = right_p[0] + 1, right_p[1]
            if right_tile == WIDE_BOX_RIGHT:
                next_left = right_p[0] - 1, right_p[1]
                next_right = right_p
            try_move_wbox(warehouse, bounds, next_left, next_right, instruction)
        
        # We assume that we have already checked whether the vertical move has been allowed before or not!
        # Move the whole box up/down by 1.
        warehouse[left_p[1]][left_p[0]] = WIDE_BOX_LEFT
        warehouse[right_p[1]][right_p[0]] = WIDE_BOX_RIGHT
        warehouse[left[1]][left[0]] = SPACE
        warehouse[right[1]][right[0]] = SPACE
        return True
    return False
    
def try_move2(warehouse, bounds, pos, instruction):
    if instruction == RIGHT:
        instruction = instruction
    result = pos
    x, y = pos[0], pos[1]
    move = get_move_direction(instruction)
    px, py = x + move[0], y + move[1]
    tile = warehouse[py][px]
    if tile == SPACE:
        result = (px, py)
    elif tile in (WIDE_BOX_LEFT, WIDE_BOX_RIGHT):
        left = (px, py)
        right = (px + 1, py)
        allow_move = True
        if tile == WIDE_BOX_RIGHT:
            left = (px - 1, py)
            right = (px, py)
        if instruction in (UP, DOWN):
            allow_move = check_vmove_wbox(warehouse, bounds, left, right, instruction)
        if allow_move: try_move_wbox(warehouse, bounds, left, right, instruction)
        if warehouse[py][px] == SPACE:
            result = (px, py)
    return result
    
def gps_values_for_type(warehouse, bounds, type):
    return [100 * box[1] + box[0] for box in get_tiles_of_type(warehouse, bounds, type)]

def print_warehouse(warehouse, robot):
    [print(''.join(row) if y != robot[1] else ''.join(row[0:robot[0]] + ['@'] + row[robot[0] + 1:])) for y, row in enumerate(warehouse)]

def part1(input):
    warehouse, bounds, robot, sequence = read_input(input)
    for instruction in sequence:
        robot = try_move(warehouse, bounds, robot, get_move_direction(instruction))
    print("Part 1: The sum of all boxes' final GPS coordinates is {}." .format(sum(gps_values_for_type(warehouse, bounds, BOX))))

def part2(input):
    warehouse, bounds, robot, sequence = read_input2(input)
    for instruction in sequence:
        robot = try_move2(warehouse, bounds, robot, instruction)
    print("Part 2: The sum of all boxes' final GPS coordinates is {}.".format(sum(gps_values_for_type(warehouse, bounds, WIDE_BOX_LEFT))))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)