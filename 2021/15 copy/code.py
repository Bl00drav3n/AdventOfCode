import math
import heapq

test_input = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''

def read_input(input):
    return [[int(entry) for entry in row] for row in input.strip().split('\n')]

def expand(grid):
    width = len(grid[0])
    height = len(grid)
    new_grid = [[0 for i in range(5 * width)] for j in range(5 * height)]
    for j in range(0, 5):
        for i in range(0, 5):
            for y in range(height):
                for x in range(width):
                    new_grid[j * height + y][i * width + x] = (grid[y][x] + i + j - 1) % 9 + 1
    return new_grid

def min_dist(dist, Q):
    d = math.inf
    p = None
    # TODO(rav3n): slow
    for y in range(len(dist)):
        for x in range(len(dist[y])):
            if (x, y) in Q and dist[y][x] < d:
                d = dist[y][x]
                p = (x, y)
    return p

def dijkstra(grid):
    distances = [[math.inf if i != 0 or j != 0 else 0 for i in range(len(grid[j]))] for j in range(len(grid))]
    Q = set()
    heapq.heapify([[Q.add((i,j)) for i in range(len(grid[j]))] for j in range(len(grid))])
    width = len(grid[0])
    height = len(grid)
    while Q:
        p = min_dist(distances, Q)
        Q.remove(p)
        x, y = p
        d = distances[y][x]
        if x == width - 1 and y == height - 1:
            return d
        for u, v in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
            if u >= 0 and u < width and v >= 0 and v < height and (u, v) in Q:
                if d + grid[v][u] < distances[v][u]:
                    distances[v][u] = d + grid[v][u]
    return math.inf

def part1(input):
    grid = read_input(input)
    #min_risk = dijkstra(grid)
    #print("Part 1: The lowest total risk for any path is {}".format(min_risk))

def part2(input):
    grid = read_input(input)
    grid = expand(grid)
    min_risk = dijkstra(grid)
    print("Part 2: The lowest total risk for any path is {}".format(min_risk))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)