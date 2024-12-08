test_input = '''
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''

def read_input(input):
    antennas = {}
    lines = input.strip().split('\n')
    bounds = len(lines[0]), len(lines)
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            if value != '.':
                if not value in antennas:
                    antennas[value] = []
                antennas[value].append((x,y))
    return antennas, bounds

def check_bounds(bounds, location):
    return location[0] >= 0 and location[1] >= 0 and location[0] < bounds[0] and location[1] < bounds[1]

def find_all_locations(locations, bounds, antenna, delta):
    antinode = antenna
    while True:
        antinode = (antinode[0] + delta[0], antinode[1] + delta[1])
        if check_bounds(bounds, antinode):
            if not antinode in locations: locations.add(antinode)
        else:
            break

def solve(input):
    antennas, bounds = read_input(input)
    antenna_locations = set()
    for locations in antennas.values():
        antenna_locations |= set(locations)
    unq_loc = set()
    unq_loc2 = set()
    for _, locations in antennas.items():
        for i in range(len(locations)):
            a = locations[i]
            for j in range(i + 1, len(locations)):
                b = locations[j]
                dx = b[0] - a[0]
                dy = b[1] - a[1]

                #Part 1
                antinodes = ((a[0] - dx, a[1] - dy), (b[0] + dx, b[1] + dy))
                if check_bounds(bounds, antinodes[0]) and not antinodes[0] in unq_loc: unq_loc.add(antinodes[0])
                if check_bounds(bounds, antinodes[1]) and not antinodes[1] in unq_loc: unq_loc.add(antinodes[1])

                #Part 2
                find_all_locations(unq_loc2, bounds, b, (-dx, -dy))
                find_all_locations(unq_loc2, bounds, a, (dx, dy))
                
    return len(unq_loc), len(unq_loc2)

def part1(input):
    count, _ = solve(input)
    print("Part 1: There are {} unique locations inside the map bounds.".format(count))

def part2(input):
    _, count = solve(input)
    print("Part 2: There are {} unique locations inside the map bounds.".format(count))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)