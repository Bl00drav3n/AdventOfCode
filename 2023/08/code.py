test_input = '''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)'''

test_input2 = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''

test_input3 = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''

from dataclasses import dataclass
from itertools import cycle

@dataclass
class Node:
    left: str
    right: str

    def next_node(self, ins):
        return self.left if ins == 'L' else self.right

def parse_line(line) -> (str, Node):
    key, value = line.split(' = ')
    l, r = value[1:-1].split(', ')
    return key, Node(left=l, right=r)

def get_path_length(network, instruction_string, nodestr) -> (int, str):
    # Given a network, instructions and a starting node, find the end node (result) and the number of steps it takes to reach it (count)
    result = None
    node = network[nodestr]
    for count, ins in enumerate(cycle(instruction_string)):
        next_node_key = node.next_node(ins)
        node = network[next_node_key]
        if next_node_key[-1] == 'Z':
            result = next_node_key
            break
    return count, result

def rotate_string(s, count) -> str:
    # Rotate the string to the left by count: rotate("ABCD", 2) -> "CDAB"
    offset = count % len(s)
    return (s + s)[offset:offset+len(s)]

def part1(input):
    instruction_string, network_string = input.strip().split('\n\n')
    network = {key: node for key, node in [parse_line(line) for line in network_string.split('\n')]}
    count, _ = get_path_length(network, instruction_string, 'AAA')
    print("Part 1: {} steps are required to reach ZZZ".format(count+1))

def part2(input):
    # We assume that in the end, all paths end up in an eternal cycle. We have to figure out, when all
    # the cycles land on the respective path's end node.
    instruction_string, network_string = input.strip().split('\n\n')
    network = {key: node for key, node in [parse_line(line) for line in network_string.split('\n')]}
    nodes = [key for key in network.keys() if key[-1] == 'A']
    # NOTE: Brute force approach (which was removed) does only work for the test cases
    # a contains the length of every path from each starting node to the end node
    a = [get_path_length(network, instruction_string, node) for node in nodes]
    # b contains the length of each cycle for each end node
    b = [get_path_length(network, rotate_string(instruction_string, length - 1), node) for length, node in a]
    # TODO: If the cycles would all start at the same time, the answer would be the least common multiple of the cycle lengths in b.
    #       Unfortunately, we don't start every cycle on the same step, so we have to correct by the offsets given by the lengths in a.
    print("Part 2: It takes {} steps before all nodes end with Z".format('?'))

print('---TEST---')
part1(test_input2)
part2(test_input3)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)