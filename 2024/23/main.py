test_input = '''
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
'''

import time

class Computer():
    def __init__(self, name):
        self.name = name
        self.connections = set()

    def add_connection(self, name):
        self.connections.add(name)

def read_input(input):
    computers_by_name = {}
    for line in input.strip().split('\n'):
        a, b = line.split('-')
        if not a in computers_by_name:
            computers_by_name[a] = Computer(a)
        if not b in computers_by_name:
            computers_by_name[b] = Computer(b)
        computers_by_name[a].connections.add(b)
        computers_by_name[b].connections.add(a)
    return computers_by_name

def find_networks_of_three(computers_by_name, computers):
    networks_of_three = set()
    for computer in computers:
        for connection_a in computer.connections:
            computer_a = computers_by_name[connection_a]
            for connection_b in computer_a.connections:
                computer_b = computers_by_name[connection_b]
                if computer != computer_a and computer != computer_b and computer_a != computer_b:
                    if computer.name in computer_b.connections:
                        network = tuple(sorted([computer.name, computer_a.name, computer_b.name]))
                        networks_of_three.add(network)
    return networks_of_three

def check(computers_by_name, network, computer):
    for c in network: 
        if not computer.name in computers_by_name[c].connections:
            return False
    return True

def print_time_diff(start, end):
    print("Time: {:.3f} sec".format((end - start)/1e9))

def part1(input):
    start = time.time_ns()
    computers_by_name = read_input(input)
    networks_of_three = find_networks_of_three(computers_by_name, filter(lambda c: c.name[0] == 't', computers_by_name.values()))    
    end = time.time_ns()
    
    print("Part 1: The number of three interconnected computers that contain at least one computer starting with t is {}." .format(len(networks_of_three)))
    print_time_diff(start, end)

def part2(input):
    start = time.time_ns()
    computers_by_name = read_input(input)
    networks = find_networks_of_three(computers_by_name, computers_by_name.values())
    
    # Pure bruteforce and not pretty :)
    # For every network, we try adding a new computer by checking
    # if all computeres in the network are connected to the new computer.
    # If the check succeeds, we add the new network to the next list to check.
    # We keep doing this until adding new computers doesn't find new networks.
    test_length = 3
    while networks:
        test_length += 1
        print("Testing networks of length {}...".format(test_length))
        new_networks = set()
        computers = set(computers_by_name.values())
        while computers:
            computer = computers.pop()
            for network in filter(lambda n: not computer.name in n, networks):
                if check(computers_by_name, network, computer):
                    network = tuple(sorted(list(network) + [computer.name]))
                    new_networks.add(network)
        if not new_networks:
            break
        networks = new_networks
    
    assert len(networks) == 1, "Multiple maximal networks found!"

    end = time.time_ns()
    print("Part 2: The password is {}." .format(','.join(networks.pop())))
    print_time_diff(start, end)

print('---TEST---')
part1(test_input)
part2(test_input)

with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)
