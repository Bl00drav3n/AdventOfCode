test_input = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''

def find_neighbors(field, x, y):
    min_x = x - 1 if x > 0 else x
    max_x = x + 1 if x < len(field[y]) - 1 else x
    min_y = y - 1 if y > 0 else y
    max_y = y + 1 if y < len(field) - 1 else y
    return [(i, j) for i in range(min_x, max_x + 1) for j in range(min_y, max_y + 1) if not (i == x and j == y)]

# Returns number of flashes
def step(field):
    # Literally just do what it says in the text
    p_full = []
    for y in range(len(field)):
        for x in range(len(field[y])):
            if field[y][x] < 9:
                field[y][x] += 1
            else:
                field[y][x] = 0
                p_full.append((x, y))
    # Keep adding locations where the energy is full until we don't find any, ignore locations with value 0 (already flashed)
    for p in p_full:
        x, y = p
        neighbors = find_neighbors(field, x, y)
        for n in neighbors:
            nx, ny = n
            if field[ny][nx] > 0 and field[ny][nx] < 9:
                field[ny][nx] += 1
            else:
                if field[ny][nx] != 0:
                    field[ny][nx] = 0
                    p_full.append((nx, ny))
    return len(p_full)

def draw(field):
    [print(''.join([str(val) for val in row])) for row in field]

def part1(input):
    n = 100
    field = [[int(c) for c in line] for line in input.strip().split('\n')]
    count = sum([step(field) for i in range(n)])
    print("Part 1: There are {} total flashes after {} steps".format(count, n))

def part2(input):
    field = [[int(c) for c in line] for line in input.strip().split('\n')]
    count = 0
    n = 0
    while True:
        n += 1
        step(field)
        # Only when all levels are 0, the total sum will be 0 -> synchronized
        total = sum([sum(row) for row in field])
        if total == 0:
            break
    print("Part 2: The first step during which all octopuses flash is {}".format(n))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)