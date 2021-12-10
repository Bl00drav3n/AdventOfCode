from functools import reduce
import functools

test_input = '''2199943210
3987894921
9856789892
8767896789
9899965678'''

def read_input(input):
    return [[int(digit) for digit in line] for line in input.strip().split('\n')]

def get_neighbor_locations(field, x, y):
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < len(field[y]) - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < len(field) - 1:
        neighbors.append((x, y + 1))
    return neighbors

def get_neighbors(field, x, y):
    return [field[p[1]][p[0]] for p in get_neighbor_locations(field, x, y)]

def is_low_point(field, x, y):
    return functools.reduce(lambda x, y: x and y, [field[y][x] < height for height in get_neighbors(field, x, y)])

def get_low_point_locations(field):
    return functools.reduce(lambda x, y: x + y, [[(x, y) for x in range(len(field[y])) if is_low_point(field, x, y)] for y in range(len(field))])

def get_low_points(field):
    return [field[p[1]][p[0]] + 1 for p in get_low_point_locations(field)]

def find_basin(basin, field, visited, x, y):
    if visited[y][x]:
        return
    visited[y][x] = True
    basin.append(field[y][x])
    for p in get_neighbor_locations(field, x, y):
        neighbor = field[p[1]][p[0]]
        if neighbor != 9 and neighbor > field[y][x]:
            find_basin(basin, field, visited, p[0], p[1])

def find_basins(field):
    low_points = get_low_point_locations(field)
    basin_sizes = []
    for p in low_points:
        visited = [[False for i in range(len(field[0]))] for j in range(len(field))]
        basin = []
        find_basin(basin, field, visited, p[0], p[1])
        basin_sizes.append(len(basin))
    return basin_sizes

def part1(input):
    field = read_input(input)
    risk_level = sum(get_low_points(field))
    print("Part 1: The sum of the risk levels of all low points is {}".format(risk_level))

def part2(input):
    field = read_input(input)
    basin_sizes = find_basins(field)
    print("Part 2: The product of the sizes of the 3 largest basins is {}".format(functools.reduce(lambda x, y: x * y, sorted(basin_sizes, reverse=True)[:3])))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)