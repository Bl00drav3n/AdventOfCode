test_input = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''

GUARD = '^'
OBSTRUCTION = '#'

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def find_guard(m):
    for y in range(len(m)):
        for x in range(len(m[y])):
            if m[y][x] == '^':
                return x, y
    assert False, "Guard not found!"

def in_bounds(pos, m):
    width, height = len(m[0]), len(m)
    return pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height

def rotate90(facing):
    return (facing + 1) % 4

def move(guard, facing, m, states):
    # Very bruteforce but it's fine
    x, y = guard

    # Loop detection
    state = (x, y, facing)
    active = not state in states
    if not active:
        active = active
    if active:
        # Record state
        states.add(state)

        # Try moving
        if(facing == UP):    y -= 1
        if(facing == DOWN):  y += 1
        if(facing == LEFT):  x -= 1
        if(facing == RIGHT): x += 1

        active = in_bounds((x, y), m)
        if active:
            if m[y][x] == OBSTRUCTION:
                # Reset move, only rotate
                facing = rotate90(facing)
                x, y = guard

    return (x, y), facing, active

def find_visited(m):
    visited = [[0 for _ in line] for line in m]
    states = set()
    guard = find_guard(m)
    facing = UP
    active = True
    while active:
        visited[guard[1]][guard[0]] = 1
        guard, facing, active = move(guard, facing, m, states)
    return visited

def part1(input):
    m = input.strip().split('\n')
    visited = find_visited(m)
    
    total_distinct_visits = sum([sum(row) for row in visited])
    print("Part 1: The guard will visit {} distinct positions on the map.".format(total_distinct_visits))

def part2(input):
    m = input.strip().split('\n')

    visited = find_visited(m)
    
    loops = 0
    for y in range(len(visited)):
        for x in range(len(visited[y])):
            if visited[y][x] and not m[y][x] == GUARD:
                new_m = m.copy()
                new_m[y] = new_m[y][:x] + '#' + new_m[y][x+1:]
                guard = find_guard(m)
                states = set()
                facing = UP
                active = True
                while active:
                    guard, facing, active = move(guard, facing, new_m, states)
                    if not active and in_bounds(guard, new_m):
                        loops += 1
    print("Part 2: You could choose {} different positions for the obsruction.".format(loops))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)

    import time
    start = time.time_ns()
    part2(input)
    end = time.time_ns()
    print("Runtime: {:.3f} sec.".format((end - start) / (10 ** 9)))