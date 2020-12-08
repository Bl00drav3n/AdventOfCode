test_input = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
'''

class interpreter:
    STATUS_OK = 0
    STATUS_LOOP_DETECTED = 1

    def __init__(self, input):
        self.a = 0
        self.pc = 0
        self.code = input[:]
        self.hitcount = [0 for ins in self.code]
        self.instructions = {
            'acc': self.acc,
            'jmp': self.jmp,
            'nop': self.nop,
        }

    def info(self):
        print('a: {} pc: {}'.format(self.a, self.pc + 1))

    def patch(self, line_nr, text):
        self.code[line_nr] = text
        return self

    def nop(self, value):
        self.pc += 1

    def acc(self, value):
        self.a += value
        self.pc += 1
    
    def jmp(self, value):
        self.pc += value

    def exec(self):
        if self.pc >= len(self.code):
            self.status = interpreter.STATUS_OK
            return False
        else:
            self.hitcount[self.pc] += 1
            if self.hitcount[self.pc] > 1:
                self.status = interpreter.STATUS_LOOP_DETECTED
                return False
            
            ins, value = tuple(self.code[self.pc].split(' '))
            self.instructions[ins](int(value))
        return True

    def run(self):
        while self.exec():
            pass
        return self.status

def patch_program(input):
    code = input.splitlines()
    for i, line in enumerate(code):
        ins, value = code[i].split(' ')
        if ins == 'acc':
            continue

        if ins == 'jmp':
            ins = 'nop'
        elif ins == 'nop':
            ins = 'jmp'
        
        interp = interpreter(code)
        status = interp.patch(i, ' '.join([ins, value])).run()
        if status == interpreter.STATUS_OK:
            print("Program exited normally with result ", interp.a)
            break

print("Patch program (TEST)...")
patch_program(test_input)

with open('input.txt') as file:
    print('Patch program...')
    patch_program(file.read())
    