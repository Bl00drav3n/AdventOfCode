test_input = '''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''

import math

def shortest_path(corrupted, width, height):
    # Inefficient Dijkstra's algorithm
    start = (0, 0)
    dest = (width - 1, height - 1)
    
    prev = {}
    dist = {}
    for y in range(height):
        for x in range(width):
            p = (x, y)
            if not p in corrupted:
                dist[p] = math.inf
                prev[p] = None
    dist[start] = 0

    q = []
    for node in dist.keys():
        q.append(node)
    while q:
        d = min([dist[node] for node in q])
        p = [node for node in q if dist[node] == d]
        p = p[0]
        if p == dest:
            break

        q.remove(p)
        x, y = p
        d += 1
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for neighbor in neighbors:
            if neighbor in q:
                if d < dist[neighbor]:
                    dist[neighbor] = d
                    prev[neighbor] = p
    
    path = []
    node = dest
    if prev[node] or node == start:
        while node:
            path.append(node)
            node = prev[node]
    return list(reversed(path))

def print_map(width, height, corrupted, path):
    for y in range(height):
        values = [None] * width
        for x in range(width):
            p = (x, y)
            value = '.'
            if p in path:
                value = 'O'
            elif p in corrupted:
                value = '#'
            values[x] = value
        print("".join(values))

def read_input(input):
    return [(int(pair[0]), int(pair[1])) for pair in [line.split(',') for line in input.strip().split('\n')]]

def part1(input, width, height, num_bytes):
    corrupted = set(read_input(input)[:num_bytes])
    path = shortest_path(corrupted, width, height)
    print("Part 1: The minimum number of steps needed to reach the exit is {}." .format(len(path) - 1))

def part2(input, width, height):
    corrupted_bytes = read_input(input)
    left = 0
    right = len(corrupted_bytes)
    # Binary search
    while left + 1 != right and left != right:
        index = (left + right) // 2
        path = shortest_path(corrupted_bytes[:index], width, height)
        pathlen = len(path)
        if pathlen:
            left = index
        else:
            right = index
    if pathlen:
        index = right
    print("Part 2: The coordinates of the first byte that will prevent the exit from being reachable from the starting position is {}.".format(",".join(str(c) for c in corrupted_bytes[index-1])))

print('---TEST---')
part1(test_input, 7, 7, 12)
part2(test_input, 7, 7)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input, 71, 71, 1024)
    part2(input, 71, 71)