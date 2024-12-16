test_input = '''
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''

START = 'S'
END = 'E'
PATH = '.'
WALL = '#'

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Direction:
    def __init__(self, state):
        self.state = state

    def __repr__(self):
        return str(self.state)

    def turn_clockwise(self):
        return Direction((self.state + 1) % 4)
    
    def turn_anticlockwise(self):
        return Direction((self.state + 3) % 4)

class Node:
    def __init__(self, p):
        self.p = p
        self.neighbors = [None, None, None, None]

    def __repr__(self):
        return "{}".format(self.p)
    
    
    def add_neighbor(self, dir, node):
        assert dir >= 0 and dir < len(self.neighbors), "Invalid direction!"
        self.neighbors[dir] = node

class Maze:
    def __init__(self):
        self.node_table = {}
        self.start = None
        self.end = None

    def read(self, input):
        lines = input.strip().split('\n')
        for y, line in enumerate(lines):
            for x, tile in enumerate(line):
                if tile != WALL:
                    p = (x, y)
                    node = Node(p)
                    self.node_table[p] = node
                    if tile == START:
                        self.start = node
                    elif tile == END:
                        self.end = node
        for pos, node in self.node_table.items():
            x, y = pos
            neighbors = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
            for dir, n in enumerate(neighbors):
                if n in self.node_table:
                    node.add_neighbor(dir, self.node_table[n])
        return self
    
    def find_lowest_score_paths(self):
        # TODO (never?): Figure out if we should go forward with this bad algorithm or rewrite it with using
        # line segments for clarity (and speed/memory footprint?).
        # The algorithm visits all connected nodes and records the best score inside the visited map.
        # Runtime is attrocious.
        states = [(self.start, Direction(EAST), 0)]
        visited = {}
        paths = {}
        path = []
        while states:
            node, dir, score = states.pop()
            path.append(node)
            if not node in visited or score <= visited[node]:
                visited[node] = score
                if node != self.end:
                    if node.neighbors:
                        directions = [dir, dir.turn_clockwise(), dir.turn_anticlockwise()]
                        score_increases = [0, 1000, 1000]
                        for i in (0, 1, 2):
                            new_dir = directions[i]
                            if node.neighbors[new_dir.state]:
                                states.append((node.neighbors[new_dir.state], new_dir, score + score_increases[i] + 1))
                else:
                    if not visited[self.end] in paths:
                        paths[visited[self.end]] = []
                    paths[visited[self.end]].append(set(path))

        best_paths = paths[visited[self.end]]
        return visited[self.end], best_paths
    
def print_paths(input, best_paths):
    for y, line in enumerate(input.strip().split('\n')):
        row = [None] * len(line)
        for x, c, in enumerate(line):
            row[x] = c
            if c in (START, END, PATH):
                for path in best_paths:
                    if (x, y) in path:
                        row[x] = 'O'
        print("".join(row))

def part1(input):
    maze = Maze().read(input)
    min_score, best_paths = maze.find_lowest_score_paths()
    print("Part 1: The lowest score a Reindeer could possibly get is {}." .format(min_score))
    part2(best_paths)

def part2(best_paths):
    print("Part 2 (FIXME!): {} tiles are part of at least one of the best paths.".format(len(set.union(*best_paths))))

print('---TEST---')
part1(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)