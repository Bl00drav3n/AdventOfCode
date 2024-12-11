test_input = '''125 17'''

def add_count(stones, number, count):
    if not number in stones:
        stones[number] = 0
    stones[number] += count

def split_number(number):
    n1 = number[:len(number)//2]
    n2 = number[len(number)//2:].lstrip('0')
    return n1, n2 if n2 else '0'

def blink(stones):
    stones_next = {}
    for number, count in stones.items():
        if number == '0': add_count(stones_next, '1', count)
        elif len(number) % 2 == 0:
            n1, n2 = split_number(number)
            add_count(stones_next, n1, count)
            add_count(stones_next, n2, count)
        else:
            add_count(stones_next, str(int(number) * 2024), count)
    return stones_next

def initial_state(input):
    stones = input.strip().split(' ')
    stone_dict = {}
    for number in stones:
        if not number in stone_dict:
            stone_dict[number] = 0
        stone_dict[number] += 1
    return stone_dict

def process(input, iterations):
    # We just keep track of what stones and how many of them are in the line and
    # just iterate on that state.
    stone_dict = initial_state(input)
    for _ in range(iterations): stone_dict = blink(stone_dict)
    return sum(stone_dict.values())
            
def part1(input):
    iterations = 25
    value = process(input, iterations)
    print("Part 1: There are {} stones after blinking {} times.".format(value, iterations))

def part2(input):
    iterations = 75
    value = process(input, iterations)
    print("Part 2: There are {} stones after blinking {} times.".format(value, iterations))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)