class CPU():
    def __init__(self):
        self.registers = [0, 0, 0, 0]
        self.reset = [0, 0, 0, 0]
        self.ops = [
            self.eqir,
            self.addi,
            self.gtir,
            self.setr,
            self.mulr,
            self.seti,
            self.muli,
            self.eqri,
            self.bori,
            self.bani,
            self.gtrr,
            self.eqrr,
            self.addr,
            self.gtri,
            self.borr,
            self.banr
        ]
 
    def op(self, ins):
        self.ops[ins[0]](ins[1], ins[2], ins[3])
 
    def save(self):
        self.reset[0] = self.registers[0]
        self.reset[1] = self.registers[1]
        self.reset[2] = self.registers[2]
        self.reset[3] = self.registers[3]
 
    def load(self):
        self.registers[0] = self.reset[0]
        self.registers[1] = self.reset[1]
        self.registers[2] = self.reset[2]
        self.registers[3] = self.reset[3]
 
    def print(self):
        print(self.registers)
   
    def addr(self, A, B, C):
        self.registers[C] = self.registers[A] + self.registers[B]
   
    def addi(self, A, B, C):
        self.registers[C] = self.registers[A] + B
 
    def mulr(self, A, B, C):
        self.registers[C] = self.registers[A] * self.registers[B]
   
    def muli(self, A, B, C):
        self.registers[C] = self.registers[A] * B
 
    def banr(self, A, B, C):
        self.registers[C] = self.registers[A] & self.registers[B]
 
    def bani(self, A, B, C):
        self.registers[C] = self.registers[A] & B
 
    def borr(self, A, B, C):
        self.registers[C] = self.registers[A] | self.registers[B]
 
    def bori(self, A, B, C):
        self.registers[C] = self.registers[A] | B
 
    def setr(self, A, B, C):
        self.registers[C] = self.registers[A]
   
    def seti(self, A, B, C):
        self.registers[C] = A
 
    def gtir(self, A, B, C):
        self.registers[C] = 1 if A > self.registers[B] else 0
 
    def gtri(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] > B else 0
 
    def gtrr(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] > self.registers[B] else 0
   
    def eqir(self, A, B, C):
        self.registers[C] = 1 if A == self.registers[B] else 0
 
    def eqri(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] == B else 0
 
    def eqrr(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] == self.registers[B] else 0
 
with open('input1.txt') as f:
    cpu = CPU()
    samples = dict([(i, []) for i in range(0, 16)])
    while True:
        initial = list(map(int, f.readline().split(":")[1].strip()[1:-1].replace(' ', '').split(',')))
        ins = list(map(int, f.readline().strip().split(' ')))
        final = list(map(int, f.readline().split(":")[1].strip()[1:-1].replace(' ', '').split(',')))
        samples[ins[0]].append((initial, ins, final))
       
        if not f.readline():
            break
 
    stats = {}
    for opcode in samples.keys():
        candidates = []
        for op in cpu.ops:
            failed = False
            for initial, ins, final in samples[opcode]:
                cpu.registers = list(initial)
                op(ins[1], ins[2], ins[3])
                if not cpu.registers == final:
                    failed = True
                    #print("operation failed", opcode, op.__name__, initial, ins, final)
                    break
                else:
                    #print("operation succeeded", opcode, op.__name__, initial, ins, final)
                    pass
            if not failed:
                candidates.append(op)
        stats[opcode] = list(map(lambda x: x.__name__, candidates))
    for key in stats.keys():
        print(key, stats[key])
 
    #print(0, "samples behave like three or more opcodes.")
 
with open('input2.txt') as f:
    cpu = CPU()
    cpu.print()
    for line in f:
        ins = list(map(int, line.strip().split(' ')))
        cpu.op(ins)
        #cpu.print()
    cpu.print()