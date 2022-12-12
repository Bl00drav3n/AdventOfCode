test_input = '''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''

def get_height(heightmap, x, y):
    height = heightmap[y][x]
    return ord('a' if height == 'S' else 'z' if height == 'E' else height) - ord('a')

def can_move(height, next_height):
    return next_height - height <= 1

def find_endpoints(heightmap):
    start = None
    end = None
    for y, row in enumerate(heightmap):
        x = row.find('S')
        if x >= 0:
            start = (x, y)
        x = row.find('E')
        if x >= 0:
            end = (x, y)
    return start, end

def should_keep(heightmap, p):
    x, y = p
    for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if nx >= 0 and nx < len(heightmap[0]) and ny >= 0 and ny < len(heightmap):
            n = heightmap[ny][nx]
            if n in ('a', 'b'):
                return True
    return False

def find_lowest_elevations(heightmap):
    points = []
    for y, row in enumerate(heightmap):
        for x, c in enumerate(row):
            if c == 'a' or c == 'S':
                points.append((x, y))
    return [p for p in points if should_keep(heightmap, p)]

def print_the_thing(heightmap, x, y):
    for j in range(len(heightmap)):
        if j == y:
            print(heightmap[j][:x] + '#' + heightmap[j][x+1:])
        else:
            print(heightmap[j])
    print()

def print_distances(distances):
    [print(' '.join(list(map(lambda x: '{:3d}'.format(x) if x != 9876543210 else ' -1', row)))) for row in distances]
    print()

def traverse(heightmap, start, end):
    distances = [[9876543210 for _ in range(len(heightmap[0]))] for _ in range(len(heightmap))]
    queue = [(start[0], start[1], 0)]
    i = 0
    while queue:
        x, y, length = queue.pop(0)
        height = get_height(heightmap, x, y)
        neighbors = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        for n in neighbors:
            nx, ny = n
            if nx >= 0 and nx < len(heightmap[0]) and ny >= 0 and ny < len(heightmap):
                next_height = get_height(heightmap, nx, ny)
                if can_move(height, next_height):
                    if distances[ny][nx] > length + 1:
                        distances[ny][nx] = length + 1
                        queue.append((nx, ny, length + 1))
    return distances[end[1]][end[0]]

def part1(input):
    if input:
        heightmap = input.strip().split('\n')
        start, end = find_endpoints(heightmap)
        min_distance = traverse(heightmap, start, end)
        print("Part 1: {}".format(min_distance))

def part2(input):
    heightmap = input.strip().split('\n')
    _ , end = find_endpoints(heightmap)
    points = find_lowest_elevations(heightmap)
    min_distance = 9876543210
    for point in points:
        min_distance = min(traverse(heightmap, point, end), min_distance)
    print("Part 2: {}".format(min_distance))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)