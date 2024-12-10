test_input = '''
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''

def read_map(input):
    trails = []
    grid = [[int(value) if value != '.' else -1 for value in row] for row in input.strip().split('\n')]
    for y, row in enumerate(grid):
        for x, height in enumerate(row):
            if height == 0:
                trails.append((x, y))
    return grid, trails
 
def trails(grid, node, visited, part2):
    height = grid[node[1]][node[0]]
    if height == 9:
        if part2:
            return 1
        else:
            if not node in visited:
                visited.add(node)
                return 1
            else:
                return 0
 
    subresult = 0
    neighbors = [
        (node[0] - 1, node[1]),
        (node[0] + 1, node[1]),
        (node[0], node[1] - 1),
        (node[0], node[1] + 1)
    ]
    for neighbor in neighbors:
        if neighbor[0] >= 0 and neighbor[0] < len(grid[0]) and neighbor[1] >= 0 and neighbor[1] < len(grid):
            neighbor_height = grid[neighbor[1]][neighbor[0]]
            if neighbor_height == height + 1:
                subresult += trails(grid, neighbor, visited, part2)
    return subresult

def part1(input):
    grid, trailheads = read_map(input)
    scores = [trails(grid, trailhead, set(), False) for trailhead in trailheads]
    print("Part 1: The sum of the scores of all trailheads is {}.".format(sum(scores)))

def part2(input):
    grid, trailheads = read_map(input)
    ratings = [trails(grid, trailhead, None, True) for trailhead in trailheads]
    print("Part 2: The sum of the ratings of all trailheads is {}.".format(sum(ratings)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)