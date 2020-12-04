import functools

TREE = '#'
OPEN = '.'

test_map = '''..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#'''

def load_map(input):
    lines = input.splitlines()
    return lines, len(lines), len(lines[0])

def count_trees_for_slope(input, slope):
    x, y = slope
    tree_count = 0
    i = 0
    m, height, xwrap = load_map(input)
    for j in range(y, height, y):
        i = (i + x) % xwrap
        if m[j][i] == TREE:
            tree_count += 1
    return tree_count

def get_path_metrics(input, directions):
    counts = [count_trees_for_slope(input, direction) for direction in directions]
    prod = functools.reduce(lambda x, y: x * y, counts)
    return counts, prod

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
print("Test metrics:", get_path_metrics(test_map, slopes))
with open('input.txt') as file:
    print("Metrics:", get_path_metrics(file.read(), slopes))