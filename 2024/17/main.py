test_input = '''Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
'''

ADV = 0
BXL = 1
BST = 2
JNZ = 3
BXC = 4
OUT = 5
BDV = 6
CDV = 7
 
class CPU:
    def __init__(self, input):
        registers, program = input.strip().split('\n\n')
        registers = registers.split('\n')
        self.a_start = int(registers[0].split(': ')[1])
        self.b_start = int(registers[1].split(': ')[1])
        self.c_start = int(registers[2].split(': ')[1])
        self.instructions = [int(c) for c in program.split(': ')[1].split(',')]
        self.reset()
    
    def reset(self):
        self.a = self.a_start
        self.b = self.b_start
        self.c = self.c_start
        self.pc = 0
        self.out = []
 
    def fetch(self):
        value = self.instructions[self.pc]
        self.pc += 1
        return value
       
    def fetch_combo(self):
        result = self.fetch()
        if result == 4: result = self.a
        elif result == 5: result = self.b
        elif result == 6: result = self.b
        elif result == 7: assert False, "Invalid program!"
        return result
    
    def print(self):
        print("State: a={} b={} c={} out={}".format(self.a, self.b, self.c, self.out))
       
    def run(self):
        while self.pc >= 0 and self.pc < len(self.instructions):
            instruction = self.fetch()
            if instruction == ADV:
                value = self.fetch_combo()
                self.a = self.a >> value
            elif instruction == BXL:
                value = self.fetch()
                self.b = self.b ^ value
            elif instruction == BST:
                value = self.fetch_combo()
                self.b = value & 0x07
            elif instruction == JNZ:
                value = self.fetch()
                if self.a: self.pc = value                
            elif instruction == BXC:
                value = self.fetch()
                self.b = self.b ^ self.c
            elif instruction == OUT:
                value = self.fetch_combo()
                self.out.append(value & 0x07)
            elif instruction == BDV:
                value = self.fetch_combo()
                self.b = self.a >> value
            elif instruction == CDV:
                value = self.fetch_combo()
                self.c = self.a >> value
        return ','.join([str(n) for n in self.out])
    
def program(A):
    # The specific program in question
    B = (A & 7) ^ 1
    C = A >> B
    B = (B ^ C) ^ 6
    return B & 7
 
def part1(input):
    cpu = CPU(input)
    print("Part 1: The output is {}." .format(cpu.run()))

def part2(input):
    cpu = CPU(input)

    # The program cares only about 3+3 bits at a time to produce another 3 bit output
    # We start by trying to reproduce the last instruction in the stream, this is easily
    # done by plugging in all 3bit digits (0-7) into the specific program and check the result.
    # If the CPU would run, it would try to shift in 3 bits from A at the last instruction, but
    # A only has 3 bits worth of data left, hence we shift in 0. This is equivalent of initializing
    # our A with 0 and adding the digit to test for. To get the next instruction, we just shift A left
    # by 3 to retain the data we have already verified.
    # We also have to keep track of which digits worked, because it can happen that we dont find a match and
    # have to reset to an older state.
    stack = [(0, 0)]
    best = int(10e300)
    while stack:
        A, depth = stack.pop()
        if depth == len(cpu.instructions):
            best = min(best, A)
        else:
            for i in range(8):
                test = 8 * A + i
                if program(test) == cpu.instructions[len(cpu.instructions) - depth - 1]:
                    stack.append((test, depth + 1))

    cpu.a = best
    assert cpu.run() == ",".join([str(i) for i in cpu.instructions]), "Initial value does not produce a copy of the program!"
    print("Part 2: The lowest possible initial value for register A that causes the program to output a copy of itself is {}.".format(best))

print('---TEST---')
part1(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)