test_input = '''v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>'''

EMPTY = 0
EAST = 1
SOUTH = 2

def read_input(input):
    mapping = {'.':EMPTY, '>':EAST,'v':SOUTH}
    return [[mapping[c] for c in row] for row in input.strip().split('\n')]

def normalize_coordinates(field, x, y):
    h = len(field)
    if y < 0:
        y += h
    elif y >= h:
        y -= h
    w = len(field[y])
    if x < 0:
        x += w
    elif x >= w:
        x -= w
    return x, y

def step(field, dir):
    moves = []
    for y in range(len(field)):
        for x in range(len(field[y])):
            if dir == EAST:
                u = x + 1
                v = y
            elif dir == SOUTH:
                u = x
                v = y + 1
            u, v = normalize_coordinates(field, u, v)
            if field[y][x] == dir and field[v][u] == EMPTY:
                moves.append((x, y, u, v))
    for (x0, y0, x1, y1) in moves:
        tmp = field[y0][x0]
        field[y0][x0] = EMPTY
        field[y1][x1] = tmp

def make_state(field):
    return '\n'.join([''.join([str(x) for x in row]) for row in field])

def print_state(state):
    print(state.replace('{}'.format(EMPTY),'.').replace('{}'.format(EAST),'>').replace('{}'.format(SOUTH),'v'))
    print()

def part1(input):
    field = read_input(input)
    last_state = make_state(field)
    #print_state(last_state)
    i = 0
    while True:
        i += 1
        step(field, EAST)
        step(field, SOUTH)
        state = make_state(field)
        #print_state(state)
        if state == last_state:
            break
        last_state = state
    print("Part 1: The first step on which no cucumber moves is {}".format(i))

def part2(input):
    print("Part 2:".format())

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)