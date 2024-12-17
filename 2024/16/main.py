test_input = '''
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
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
        self.directions = {}
        self.scores = {}
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
    
    def calculate_lowest_scores(self):
        # Bruteforce BFS cause why be smart? Sorry it's slow. We find the best 'distance' to every reachable node on the map.
        # We also record the directions we came from for every node for use in part 2.
        states = [(self.start, Direction(EAST), 0), (self.start, Direction(NORTH), 1000), (self.start, Direction(SOUTH), 1000)]
        self.scores = {node: 1e300 for node in self.node_table.values()}
        while states:
            node, dir, score = states.pop()
            if score < self.scores[node] and score <= self.scores[self.end]:
                self.scores[node] = score
                self.directions[node] = dir
                if node.neighbors and node != self.end:
                    directions = [dir, dir.turn_clockwise(), dir.turn_anticlockwise()]
                    score_increases = [0, 1000, 1000]
                    for i in (0, 1, 2):
                        new_dir = directions[i]
                        if node.neighbors[new_dir.state]:
                            states.append((node.neighbors[new_dir.state], new_dir, score + score_increases[i] + 1))
        return self.scores[self.end]
    
    def find_best_nodes(self):
        # DFS from the end to start to find all visited nodes
        visited = set()
        nodes = [(self.end, self.end)]
        while nodes:
            node, prev_node = nodes.pop()
            visited.add(node)
            if node != self.start:
                neighbors = [n for n in node.neighbors if n and not n in visited]
                for neighbor in neighbors:
                    if self.scores[neighbor] < self.scores[node] or self.directions[neighbor] == self.directions[prev_node]:
                        nodes.append((neighbor, node))
        return visited

def print_paths(input, best_nodes):
    for y, line in enumerate(input.strip().split('\n')):
        row = [None] * len(line)
        for x, c, in enumerate(line):
            row[x] = c
            if c in (START, END, PATH):
                if (x, y) in best_nodes:
                    row[x] = 'O'
        print("".join(row))

def part1(input):
    maze = Maze().read(input)
    min_score = maze.calculate_lowest_scores()
    print("Part 1: The lowest score a Reindeer could possibly get is {}." .format(min_score))
    part2(input, maze)

def part2(input, maze):
    nodes = maze.find_best_nodes()
    print("Part 2: {} tiles are part of at least one of the best paths.".format(len(nodes)))

print('---TEST---')
part1(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)