test_input = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''

def read_edges(input):
    graph = {}
    for edge in [line.split('-') for line in input.strip().split('\n') if line]:
        add_edge(graph, edge[0], edge[1])
    return graph

def is_small(cave):
    return cave == cave.lower()

def add_directed_edge(graph, A, B):
    if not A in graph:
        graph[A] = []
    graph[A].append(B)

def add_edge(graph, A, B):
    add_directed_edge(graph, A, B)
    add_directed_edge(graph, B, A)

def count_paths(graph):
    count1 = 0
    count2 = 0
    stack = [('start', set(), 0)]
    while stack:
        cave, visited, twice = stack[-1]
        stack.pop()
        if cave == 'end':
            count1 += 1 if not twice else 0
            count2 += 1
            continue
        if is_small(cave) and cave in visited:
            if twice:
                continue
            twice += 1
        visited = set(visited)
        visited.add(cave)
        for other in graph[cave]:
            if other != 'start':
                stack.append((other, visited, twice))
    return count1, count2

def part1(input):
    graph = read_edges(input)
    count = count_paths(graph)[0]
    print("Part 1: There are {} paths that visit small caves at most once".format(count))

def part2(input):
    graph = read_edges(input)
    count = count_paths(graph)[1]
    print("Part 2: There are {} paths that visits one small cave at most twice".format(count))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)