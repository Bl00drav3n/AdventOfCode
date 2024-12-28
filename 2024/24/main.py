test_input = '''
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
'''

import time
import graphviz

class Gate:
    def __init__(self, a=None, b=None, op=None):
        self.a = a
        self.b = b
        self.op = op
        self.value = None
    
    def __repr__(self):
        return "{} {} {}".format(self.a, self.op, self.b)

    def tick(self, gates):
        a = gates[self.a].value
        if a == None:
            a = gates[self.a].tick(gates)
        b = gates[self.b].value
        if b == None:
            b = gates[self.b].tick(gates)
        match self.op:
            case 'AND': return a & b
            case 'OR': return a | b
            case 'XOR': return a ^ b
            case _: assert False, 'Invalid operator!'

    def dependencies(self, gates, d):
        if gates[self.a].value == None:
            gates[self.a].dependencies(gates, d)
        else:
            d.add(self.a)
        if gates[self.b].value == None:
            gates[self.b].dependencies(gates, d)
        else:
            d.add(self.b)

def read_input(input):
    state_strings, gate_strings = input.strip().split('\n\n')
    gates = {}
    for state in state_strings.split('\n'):
        wire, value = state.split(': ')
        gates[wire] = Gate()
        gates[wire].value = int(value)
    for gate_string in gate_strings.split('\n'):
        lhs, rhs = gate_string.split(' -> ')
        a, op, b = lhs.split(' ')
        gates[rhs] = Gate(a, b, op)
    return gates

def solve(gates):
    output_wires = {wire: gate.tick(gates) for wire, gate in filter(lambda item: item[0][0] == 'z', gates.items())}
    return ''.join([str(output_wires[wire]) for wire in sorted(output_wires, reverse=True)])

def print_time_diff(start, end):
    print("Time: {:.3f} sec".format((end - start)/1e9))

def part1(input):
    start = time.time_ns()
    gates = read_input(input)
    result = int(solve(gates), base=2)
    end = time.time_ns()
    
    print("Part 1: The system outputs a the number {}." .format(result))
    print_time_diff(start, end)

def part2(input):
    start = time.time_ns()
    gates = read_input(input)

    input_wires_x = sorted([wire for wire in gates.keys() if wire[0] == 'x'])
    input_wires_y = sorted([wire for wire in gates.keys() if wire[0] == 'y'])
    output_wires = sorted([wire for wire in gates.keys() if wire[0] == 'z'])

    for wire in input_wires_x:
        gates[wire].value = 0
    for wire in input_wires_y:
        gates[wire].value = 0
    
    dependencies = {}
    for wire in output_wires:
        s = set()
        gates[wire].dependencies(gates, s)
        dependencies[wire] = sorted(s)

    # TODO: The logic is flawed, we are looking at the wrong nodes!
    broken_outputs = set()
    for gate in gates:
        g = gates[gate]
        if gate[0] == 'z':
            if g.op != 'XOR':
                broken_outputs.add(gate)
        if g.a and g.b:
            a = gates[g.a]
            b = gates[g.b]
            if a.op and b.op:
                match g.op:
                    case 'XOR':
                        if not (a.op == 'XOR' and b.op == 'OR' or a.op == 'OR' and b.op == 'XOR'):
                            if not (gate == 'z01' and a.op == 'XOR' and b.op == 'AND' or a.op == 'OR' and b.op == 'XOR'):
                                broken_outputs.add(gate)
                                print("{} - {}: {}, {}".format(gate, g, a, b))
                    case 'AND':
                        if not (a.op == 'XOR' and b.op == 'OR' or a.op == 'OR' and b.op == 'XOR'):
                            broken_outputs.add(gate)
                            print("{} - {}: {}, {}".format(gate, g, a, b))
                    case 'OR':
                        if not (a.op == 'AND' and b.op == 'AND'):
                            broken_outputs.add(gate)
                            print("{} - {}: {}, {}".format(gate, g, a, b))
    result = sorted(broken_outputs)
    assert len(result) == 8, "Invalid number of wires!"
    end = time.time_ns()
    print("Part 2: The answer is {}." .format(','.join(result)))
    print_time_diff(start, end)

print('---TEST---')
part1(test_input)

with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)
