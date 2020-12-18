test_input1 = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
'''

test_input2 = '''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''

def parse_mask(tk):
    global mask
    mask = tk

def get_location(tk_mem):
    loc = int(tk_mem[tk_mem.find('[') + 1:tk_mem.rfind(']')])
    return loc

def parse_mem1(tk_mem, tk_value):
    global mem
    global mask
    loc = get_location(tk_mem)
    value = int(tk_value)
    for i, bit in enumerate(reversed(mask)):
        mask_value = 1 << i
        if bit == '0':
            value = value & ~mask_value
        elif bit == '1':
            value = value | mask_value
    mem[loc] = value

def parse_mem2(tk_mem, tk_value):
    global mem
    global mask
    base_loc = get_location(tk_mem)
    value = int(tk_value)
    perm_locs = []
    for i, bit in enumerate(reversed(mask)):
        mask_value = 1 << i
        if bit == '1':
            base_loc = base_loc | mask_value
        if bit == 'X':
            perm_locs.append(i)
    locations = [base_loc]
    for perm in perm_locs:
        mask_value = 1 << perm
        tmp = []
        for loc in locations:
            tmp.append(loc & ~mask_value)
            tmp.append(loc | mask_value)
        locations = tmp
    for loc in locations:
        mem[loc] = value

def parse_line(line, parse_mem):
    lhs, rhs = tuple(line.strip().split(' = '))
    if lhs == 'mask':
        parse_mask(rhs)
    elif lhs[:3] == 'mem':
        parse_mem(lhs, rhs)

def parse(input, parse_mem):
    global mask
    global mem
    mask = None
    mem = {}
    for line in input:
        parse_line(line, parse_mem)
    return sum(mem.values())

print('Sum of all values (TEST1):', parse(test_input1.splitlines(), parse_mem1))
print('Sum of all values (TEST2):', parse(test_input2.splitlines(), parse_mem2))
with open('input.txt') as file:
    input = file.readlines()
    print('Sum of all values part1:', parse(input, parse_mem1))
    print('Sum of all values part2:', parse(input, parse_mem2))