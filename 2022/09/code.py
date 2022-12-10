test_inputs = [
'''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
''',
'''
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
]

def clamp(x, a, b):
    return min(max(a, x), b)

def parse_input(input):
    return map(lambda x: (x[0], int(x[1])), [line.split() for line in input.strip().split('\n') if line])

# DEAR GOD HELP US
def draw_knots(minx, miny, w, h, knots):
    print()
    for y in range(miny, miny + h + 1):
        y =  miny + h - (y - miny)
        for x in range(minx, minx + w + 1):
            c = 's' if x == 0 and y == 0 else '.'
            for i in reversed(range(len(knots))):
                knot = knots[i]
                if x == knot[0] and y == knot[1]:
                    c = str(i) if i > 0 else 'H'
            print(c, end='')
        print()
    print()

def draw_visited(visited, start):
    xval = [c[0] for c in visited]
    yval = [c[1] for c in visited]
    minx = min(xval)
    maxx = max(xval)
    miny = min(yval)
    maxy = max(yval)
    print()
    for y in range(miny, maxy + 1):
        y = maxy - (y - miny)
        for x in range(minx, maxx + 1):
            c = '.'
            if (x == start[0] and y == start[1]):
                c = 's'
            elif (x, y) in visited :
                c = '#'
            print(c, end='')
        print()
    print()

def touching(head, tail):
    return max(abs(head[0] - tail[0]), abs(head[1] - tail[1])) <= 1

def update(head, tail):
    # HOW DID THIS TAKE SO LONG?!
    if not touching(head, tail):
        dx = clamp(head[0] - tail[0], -1, 1)
        dy = clamp(head[1] - tail[1], -1, 1)
        tail[0] += dx
        tail[1] += dy

def simulate(input, num_knots):
    # Gordian heccin knots
    knots = [[0, 0] for _ in range(num_knots)]
    moves = {
        'R': [1, 0],
        'U': [0, 1],
        'L': [-1, 0],
        'D': [0, -1]
    }
    visited = set()
    for heading, steps in parse_input(input):
        move = moves[heading]
        for step in range(steps):
            knots[0][0] += move[0]
            knots[0][1] += move[1]
            for i in range(len(knots) - 1):
                update(knots[i], knots[i+1])
            visited.add(tuple(knots[-1]))
    #draw_visited(visited, (0, 0))
    return len(visited)

# The actual code
def part1(input):
    result = simulate(input, 2)
    print("Part 1: {}".format(result))

def part2(input):
    result = simulate(input, 10)
    print("Part 2: {}".format(result))

print('---TEST---')
part1(test_inputs[0])
part2(test_inputs[1])
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)