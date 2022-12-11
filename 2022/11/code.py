test_input = '''
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''

# magical number of the monkeys
magic_monkey_number = None

def update_magic_monkey_number(monkeys):
    global magic_monkey_number
    magic_monkey_number = 1
    for monkey in monkeys:
        magic_monkey_number *= monkey.test

def worry_less(worry):
    return worry // 3

def worry_even_less(worry):
    # At some point we will figure out why this is true, I promise
    return worry % magic_monkey_number

def operation_add(x, y):
    return x + y if y else x + x

def operation_mul(x,  y):
    return x * y if y else x * x

class Monkey:
    def __init__(self, block):
        lines = block.split('\n')
        self.items = list(map(int, lines[1].split(':')[1].strip().split(', ')))
        opstr = lines[2].split()
        self.op = operation_add if opstr[4] == '+' else operation_mul
        self.arg = int(opstr[5]) if opstr[5] != 'old' else None
        self.test = int(lines[3].split()[3])
        self.target_true = int(lines[4].split()[5])
        self.target_false = int(lines[5].split()[5])
        self.inspect_count = 0

    def catch(self, item):
        self.items.append(item)
    
    def inspect(self, monkeys, worry_management):
        while self.items:
            self.inspect_count += 1
            item = self.items.pop(0)
            item = self.op(item, self.arg)
            item = worry_management(item)
            target = self.target_true if item % self.test == 0 else self.target_false
            monkeys[target].catch(item)
    
def parse_input(input):
    monkeys = []
    if input:
        blocks = input.strip().split('\n\n')
        for block in blocks:
            monkeys.append(Monkey(block))
    update_magic_monkey_number(monkeys)
    return monkeys

def do_the_monkey_business(input, rounds, worry_management):
    monkeys = parse_input(input)
    for round in range(rounds):
        for monkey in monkeys:
            monkey.inspect(monkeys, worry_management)
    counts = sorted([m.inspect_count for m in monkeys])[-2:]
    return counts[0] * counts[1]

def part1(input):
    business = 0
    if input:
        business = do_the_monkey_business(input, 20, worry_less)
    print("Part 1: {}".format(business))

def part2(input):
    business = 0
    if input:
        # We use our magic monkey number to reduce our worries
        business = do_the_monkey_business(input, 10000, worry_even_less)
    print("Part 2: {}".format(business))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)