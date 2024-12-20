test_input = '''
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''

import time
import math
import heapq

TRACK = '.'
WALL = '#'
START = 'S'
END = 'E'

class PriorityQueue:
    # Implementation example taken from https://docs.python.org/3/library/heapq.html
    def __init__(self, queue):
        self.queue = queue
        self.entry_lookup = {}
        self.counter = 0
    
    def __contains__(self, item):
        return item in self.entry_lookup

    def add_with_priority(self, item, priority=0):
        if item in self.entry_lookup:
            self.remove(item)
        self.counter += 1
        entry = [priority, id(item), self.counter, item]
        self.entry_lookup[item] = entry
        heapq.heappush(self.queue, entry)
    
    def remove(self, item):
        # Flag for removal by setting the item to None
        entry = self.entry_lookup.pop(item)
        entry[-1] = None

    def pop(self):
        # Clean up any removed entries for item, then return item
        while self.queue:
            priority, item_id, count, item = heapq.heappop(self.queue)
            if item:
                del self.entry_lookup[item]
                return item
        return None

class Node:
    def __init__(self, p, t):
        self.t = t
        self.p = p
        self.neighbors = []

    def __repr__(self):
        return "Position: {}, Type: {}".format(self.p, self.t)
    
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

class Racetrack:
    def __init__(self, input):
        self.start = None
        self.end = None
        self.nodes = set()
        # map of (position, node)
        self.node_lookup = {}
        
        # Read racetrack map
        lines = input.strip().split('\n')
        self.width = len(lines[0])
        self.height = len(lines)
        for y in range(self.height):
            for x in range(self.width):
                pos = (x, y)
                t = lines[y][x]
                node = Node(pos, lines[y][x])
                self.node_lookup[pos] = node
                if t != WALL:
                    self.nodes.add(node)
                    if t == START:
                        self.start = node
                    elif t == END:
                        self.end = node

        # Link up the graph
        for pos, node in self.node_lookup.items():
            neighbors = [(pos[0], pos[1] - 1), (pos[0] + 1, pos[1]), (pos[0], pos[1] + 1), (pos[0] - 1, pos[1])]
            for neighbor_pos in neighbors:
                if neighbor_pos in self.node_lookup.keys():
                    neighbor = self.node_lookup[neighbor_pos]
                    if node.t == WALL or neighbor.t != WALL:
                        node.add_neighbor(neighbor)

    def find_node_distances(self, start):
        # Dijkstra's shortest path algorithm using a priority queue
        dist = {}
        queue = []
        pq = PriorityQueue(queue)
        init_distance = math.inf
        for node in filter(lambda n: n != start, self.nodes):
            dist[node] = init_distance
            pq.add_with_priority(node, init_distance)
        start_distance = 0
        dist[start] = start_distance
        pq.add_with_priority(start, start_distance)

        while queue:
            u = pq.pop()
            if u:
                for v in filter(lambda item: item in pq, u.neighbors):
                    d = dist[u] + 1
                    if d < dist[v]:
                        dist[v] = d
                        pq.remove(v)
                        pq.add_with_priority(v, d)
        return dist

def check_cheat_savings(input, max_steps):
    # Returns a map of (path_length_difference, count)
    # The algorithm first finds the distances to every node
    # measured from the start. For each node we look at every other
    # node contained in a diamond-shaped region around it, with the size
    # determined by max_steps.
    # Example max_step = 3
    #    x
    #   xxx
    #  xxxxx
    # xxxoxxx
    #  xxxxx
    #   xxx
    #    x
    # Inside the region, walls do not exist (because we have our cheat active).
    # This means the distance from the current node o to any other node x is simply
    # the manhattan distance between them. We calculate this distance for every traversable
    # node inside the region. If the difference of the distance from the start of node x
    # and the updated distance is greater than zero, then it means that we have found
    # a path that saves time and we update the global counts for the calculated path length difference.
    racetrack = Racetrack(input)
    dist = racetrack.find_node_distances(racetrack.start)
    counts = {}
    for track_node in racetrack.nodes:
        track_node_dist = dist[track_node]
        reachable_nodes = set()
        # Construct the diamond shaped region
        for x in range(max_steps + 1):
            for y in range(max_steps + 1 - x):
                offsets = [(x, y), (-x, y), (x, -y), (-x, -y)]
                for offset in offsets:
                    pos = (track_node.p[0] + offset[0], track_node.p[1] + offset[1])
                    if pos in racetrack.node_lookup:
                        n = racetrack.node_lookup[pos]
                        if n.t != WALL:
                            reachable_nodes.add(n)
        for node in reachable_nodes:
            dx = node.p[0] - track_node.p[0]
            dy = node.p[1] - track_node.p[1]
            steps = abs(dx) + abs(dy)
            diff = dist[node] - track_node_dist - steps
            if diff > 0:
                if not diff in counts:
                    counts[diff] = 0
                counts[diff] += 1    
    return counts.items()

def print_time_diff(start, end):
    print("Time: {:.3f} sec".format((end - start)/1e9))

def part1(input, min_savings):
    start = time.time_ns()
    counts = check_cheat_savings(input, 2)
    end = time.time_ns()
    print("Part 1: There are {} cheats that would save at least {} picoseconds." .format(sum([item[1] for item in counts if item[0] >= min_savings]), min_savings))
    print_time_diff(start, end)

def part2(input, min_savings):
    start = time.time_ns()
    counts = check_cheat_savings(input, 20)
    end = time.time_ns()
    print("Part 2: There are {} cheats that would save at least {} picoseconds." .format(sum([item[1] for item in counts if item[0] >= min_savings]), min_savings))
    print_time_diff(start, end)

print('---TEST---')
part1(test_input, 2)
part2(test_input, 50)

with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input, 100)
    part2(input, 100)