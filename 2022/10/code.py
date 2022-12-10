test_input = '''
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''

class CPU:
    def __init__(self, program):
        self.X = 1
        self.ticks = 0
        self.program = iter(program.strip().split('\n'))
        self.cycles = {
            'noop': 1,
            'addx': 2
        }
        self.ins = None
        self.delay = 0

    def clock(self):
        self.ticks += 1
        if not self.ins:
            self.fetch()
        self.delay = self.delay - 1 if self.delay > 0 else 0

    def run(self):
        if self.ins:
            if self.delay == 0:
                self.addX(self.ins[1])
                self.ins = None

    def fetch(self):
        line = next(self.program, None)
        if line:
            parts = line.split()
            arg = int(parts[1]) if len(parts) > 1 else 0
            self.ins = [parts[0], arg]
            self.delay = self.cycles[parts[0]]

    def addX(self, V):
        self.X += V

def draw_crt(crt):
    [print(''.join(line)) for line in crt]
    
def part1(input):
    cpu = CPU(input)
    total = 0
    while cpu.ticks < 220:
        cpu.clock()
        if cpu.ticks == 20 or (cpu.ticks + 20) % 40 == 0:
            total += cpu.ticks * cpu.X
        cpu.run()
    print("Part 1: {}".format(total))

def part2(input):
    cpu = CPU(input)
    crt = [['.' for _ in range(40)] for _ in range(6)]
    for idx in range(40 * 6):
        x = idx % 40
        cpu.clock()
        hpos = cpu.X
        cpu.run()
        if hpos >= x - 1 and hpos <= x + 1:
            print('#', end='')
        else:
            print('.', end='')
        if x + 1 == 40:
            print()

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)