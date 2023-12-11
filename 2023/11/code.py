test_input = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''

def distance(a, b) -> int:
    # Manhattan distance (1-norm)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def adjust(galaxies, multiplier=2):
    # First generate a sorted list of x and y values for all galaxies
    xs = sorted([g[0] for g in galaxies])
    ys = sorted([g[1] for g in galaxies])
    # Some space to record adjustments for post processing
    x_adjust = [0] * len(galaxies)
    y_adjust = [0] * len(galaxies)
    # Check consecutive values in xs and ys, if they differ by more than 1, then they contain empty spaces.
    # Accumulate adjustments for each galaxy according to the number of empty spaces x (multiplier - 1).
    # Example: if the step is from 5 to 8 and the multiplier is 3 (replace 1 with 3 spaces), then the number of empty spaces is 2 and the adjustment is 4.
    # We only adjust galaxies that have values greater than or equal the greater of the two test-values.
    # TODO: Consolidate these two code branches?
    for x in zip(xs, xs[1:]):
        dx = x[1] - x[0]
        if dx > 1:
            for i in range(len(galaxies)):
                g = galaxies[i]
                if g[0] >= x[1]:
                    x_adjust[i] += (dx - 1) * (multiplier - 1)
    for y in zip(ys, ys[1:]):
        dy = y[1] - y[0]
        if dy > 1:
            for i in range(len(galaxies)):
                g = galaxies[i]
                if g[1] >= y[1]:
                    y_adjust[i] += (dy - 1) * (multiplier - 1)
    # Apply the adjustments for x and y positions
    for i in range(len(galaxies)):
        g = galaxies[i]
        galaxies[i] = (g[0] + x_adjust[i], g[1] + y_adjust[i])

def parse(input) -> list[tuple[int,int]]:
    # Galaxies are represented as integer tuples
    rows = input.strip().split('\n')
    galaxies = []
    for y, row in enumerate(rows):
        for x, sym in enumerate(row):
            if sym == '#':
                galaxies.append((x, y))
    return galaxies

def total_min_distances(galaxies) -> int:
    # Calculate manhattan distance between each pair and sum up the values
    total = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            total += distance(galaxies[i], galaxies[j])
    return total

def part1(input):
    galaxies = parse(input)
    adjust(galaxies)
    print("Part 1: The sum of the distances is {}".format(total_min_distances(galaxies)))

def part2(input):
    galaxies = parse(input)
    adjust(galaxies, multiplier=1000000)
    print("Part 1: The sum of the distances is {}".format(total_min_distances(galaxies)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)