test_text = [
    "Step C must be finished before step A can begin.",
    "Step C must be finished before step F can begin.",
    "Step A must be finished before step B can begin.",
    "Step A must be finished before step D can begin.",
    "Step B must be finished before step E can begin.",
    "Step D must be finished before step E can begin.",
    "Step F must be finished before step E can begin."
]

text = [
    "Step S must be finished before step C can begin.",
    "Step C must be finished before step R can begin.",
    "Step L must be finished before step W can begin.",
    "Step V must be finished before step B can begin.",
    "Step P must be finished before step Y can begin.",
    "Step M must be finished before step B can begin.",
    "Step Y must be finished before step J can begin.",
    "Step W must be finished before step T can begin.",
    "Step N must be finished before step I can begin.",
    "Step H must be finished before step O can begin.",
    "Step O must be finished before step T can begin.",
    "Step Q must be finished before step X can begin.",
    "Step T must be finished before step K can begin.",
    "Step A must be finished before step D can begin.",
    "Step G must be finished before step K can begin.",
    "Step D must be finished before step X can begin.",
    "Step R must be finished before step J can begin.",
    "Step U must be finished before step B can begin.",
    "Step K must be finished before step J can begin.",
    "Step B must be finished before step J can begin.",
    "Step J must be finished before step E can begin.",
    "Step E must be finished before step Z can begin.",
    "Step F must be finished before step I can begin.",
    "Step X must be finished before step Z can begin.",
    "Step Z must be finished before step I can begin.",
    "Step E must be finished before step F can begin.",
    "Step R must be finished before step I can begin.",
    "Step L must be finished before step Z can begin.",
    "Step N must be finished before step O can begin.",
    "Step O must be finished before step D can begin.",
    "Step K must be finished before step I can begin.",
    "Step R must be finished before step F can begin.",
    "Step T must be finished before step F can begin.",
    "Step N must be finished before step G can begin.",
    "Step M must be finished before step D can begin.",
    "Step F must be finished before step X can begin.",
    "Step S must be finished before step D can begin.",
    "Step Q must be finished before step F can begin.",
    "Step L must be finished before step R can begin.",
    "Step J must be finished before step F can begin.",
    "Step L must be finished before step T can begin.",
    "Step M must be finished before step H can begin.",
    "Step D must be finished before step F can begin.",
    "Step W must be finished before step B can begin.",
    "Step C must be finished before step A can begin.",
    "Step E must be finished before step I can begin.",
    "Step P must be finished before step Q can begin.",
    "Step A must be finished before step B can begin.",
    "Step P must be finished before step R can begin.",
    "Step C must be finished before step J can begin.",
    "Step Y must be finished before step K can begin.",
    "Step C must be finished before step L can begin.",
    "Step E must be finished before step X can begin.",
    "Step X must be finished before step I can begin.",
    "Step A must be finished before step G can begin.",
    "Step M must be finished before step E can begin.",
    "Step C must be finished before step T can begin.",
    "Step C must be finished before step Y can begin.",
    "Step K must be finished before step E can begin.",
    "Step H must be finished before step D can begin.",
    "Step P must be finished before step K can begin.",
    "Step D must be finished before step R can begin.",
    "Step J must be finished before step X can begin.",
    "Step H must be finished before step Z can begin.",
    "Step M must be finished before step R can begin.",
    "Step V must be finished before step U can begin.",
    "Step K must be finished before step B can begin.",
    "Step L must be finished before step Q can begin.",
    "Step Y must be finished before step I can begin.",
    "Step T must be finished before step G can begin.",
    "Step U must be finished before step E can begin.",
    "Step S must be finished before step Q can begin.",
    "Step P must be finished before step G can begin.",
    "Step P must be finished before step M can begin.",
    "Step N must be finished before step J can begin.",
    "Step P must be finished before step O can begin.",
    "Step U must be finished before step J can begin.",
    "Step C must be finished before step N can begin.",
    "Step W must be finished before step R can begin.",
    "Step B must be finished before step Z can begin.",
    "Step F must be finished before step Z can begin.",
    "Step O must be finished before step E can begin.",
    "Step W must be finished before step N can begin.",
    "Step A must be finished before step I can begin.",
    "Step W must be finished before step J can begin.",
    "Step R must be finished before step E can begin.",
    "Step N must be finished before step B can begin.",
    "Step M must be finished before step U can begin.",
    "Step B must be finished before step E can begin.",
    "Step V must be finished before step J can begin.",
    "Step O must be finished before step I can begin.",
    "Step Q must be finished before step T can begin.",
    "Step Q must be finished before step U can begin.",
    "Step L must be finished before step V can begin.",
    "Step S must be finished before step Z can begin.",
    "Step C must be finished before step P can begin.",
    "Step P must be finished before step A can begin.",
    "Step S must be finished before step G can begin.",
    "Step N must be finished before step H can begin.",
    "Step V must be finished before step H can begin.",
    "Step B must be finished before step I can begin."
]

# https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
def khan(nodes, edges):
    edges = set(edges)
    L = []
    S = nodes - set(edge[1] for edge in edges)
    while S:
        tmp = sorted(S)
        n = tmp.pop(0)
        S = set(tmp)
        L.append(n)
        for m in [edge[1] for edge in edges if edge[0] == n]:
            edges.remove((n, m))
            if not [edge for edge in edges if edge[1] == m]:
                S.add(m)
    if edges:
        raise RuntimeError("graph has at least one cycle")
    return L

#text = test_text
nodes = set()
edges = set()
for s in text:
    ss = s.split(' ')
    src, dst = ss[1], ss[7]
    edges.add((src, dst))
    nodes.add(src)
    nodes.add(dst)

#PART 1
result = ''.join(khan(nodes, edges))
print(result, len(result))

#PART 2
