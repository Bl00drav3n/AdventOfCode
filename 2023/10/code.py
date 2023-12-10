test_input = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ'''

from dataclasses import dataclass

@dataclass
class Vector:
    x: int
    y: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __hash__(self):
        return hash((self.x, self.y))

def parse(input) -> dict[tuple[Vector], str]:
    lines = input.strip().split('\n')
    chart = {}
    for y, line in enumerate(lines):
        for x, sym in enumerate(line):
            chart[Vector(x, y)] = sym
    return chart

def get_direction(start, end) -> str:
    dx = end.x - start.x
    dy = end.y - start.y
    if dx > 0:
        return "EAST"
    if dx < 0:
        return "WEST"
    if dy > 0:
        return "SOUTH"
    return "NORTH"

def opposite(direction):
    if direction == 'NORTH':
        return 'SOUTH'
    if direction == 'SOUTH':
        return 'NORTH'
    if direction == 'WEST':
        return 'EAST'
    return 'WEST'

pipe_map = {
    '|': ['NORTH', 'SOUTH'],
    '-': ['EAST', 'WEST'],
    'L': ['NORTH', 'EAST'],
    'J': ['NORTH', 'WEST'],
    '7': ['WEST', 'SOUTH'],
    'F': ['SOUTH', 'EAST'],
    '.': [],
    'S': ['NORTH', 'SOUTH', 'EAST', 'WEST']
}

def part1(input):
    chart = parse(input)
    chart = {item for item in chart.items() if item[1] != '.'}
    start_pos = [k for (k, v) in chart.items() if v == 'S'][0]
    # Find possible ways to go from the starting position
    neighbor_offsets = [Vector(-1, 0), Vector(1, 0), Vector(0, -1), Vector(0, 1)]
    ways = [n for n in neighbor_offsets if start_pos + n in chart]
    neighbors = [start_pos + n for n in ways]
    connected = []
    for n in neighbors:
        direction = get_direction(n, start_pos)
        if direction in pipe_map[chart[n]]:
            connected.append(n)

    # Traverse until we get to the start again
    count = 0
    pos = connected[0]
    direction = get_direction(start_pos, pos)
    while True:
        pipe = chart[pos]
        if pipe == 'S':
            break
        else:
            direction = [d for d in pipe_map[pipe] if d != opposite(direction)][0]
            move = Vector(0, 0)
            if direction == 'NORTH':
                move.y = -1
            elif direction == 'SOUTH':
                move.y = 1
            elif direction == 'WEST':
                move.x = -1
            else:
                move.x = 1
            pos = pos + move
            count += 1
    distance = ((count + 1) // 2)
    print("Part 1: The distance to the farthest point is {}".format(distance))

def part2(input):
    # TODO: Part2 involves figuring out the topology of the pipe system
    # In a first step, we can find the tiles corresponding to the main loop of the system by simply traversing it
    # and just keeping visited tiles. Then for all the other tiles, we have to check whether we are inside or outside the main loop.
    # What complicates matters is, that combinations like 7F, JF, 7L and JL correspond to an open gap in the system.
    # For example: This loop's ground tiles are all considered outside O
    # OOOOOOOO
    # OF----7O
    # O|F--7|O
    # O||OO||O
    # O|L7F7|O
    # OL_JL_JO
    # OOOOOOOO
    # This loop contains tiles that are considered inside I
    # OOOOOOOO
    # OF----7O
    # O|F--7|O
    # O|L7FJ|O
    # O|I||I|O
    # OL_JL_JO
    # OOOOOOOO
    print("Part 2:".format())

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)