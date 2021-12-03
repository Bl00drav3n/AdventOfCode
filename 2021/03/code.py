# We tried something fancy and it turned out to be a complicated mess. 
# It works, so we wont't change it.

test_input = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010'''

def get_mask(report):
    return (1 << len(report)) - 1

def get_bit(report, n):
    return (report >> n) & 1

def get_bitcount(n):
    if n == 0:
        return 0
    else:
        return 1 + get_bitcount(n >> 1)

def most_common_bit(reports, bit):
    return 1 if sum([get_bit(r, bit) for r in reports]) >= (len(reports) + 1) // 2 else 0

def read_pattern(pattern, mask):
    return int(pattern, 2) & mask

def get_gamma_rate(reports, mask):
    rate = 0
    for bit in range(get_bitcount(mask), -1, -1):
        rate = (rate << 1) + most_common_bit(reports, bit)
    return rate

def read_input(input):
    mask = get_mask(input[0])
    reports = [read_pattern(r, mask) for r in input]
    return reports, mask

def process_reports(reports, bit, is_co2):
    if len(reports) > 1:
        criterium = most_common_bit(reports, bit)
        if is_co2:
            criterium = 1 - criterium
        reports = [r for r in reports if get_bit(r, bit) == criterium]
    return reports

def part1(input):
    reports, mask = read_input(input)
    gamma = get_gamma_rate(reports, mask)
    epsilon = (~gamma) & mask
    print("Part 1: The power consumption of the submarine is {}", gamma * epsilon)

def part2(input):
    reports, mask = read_input(input)
    bitcount = get_bitcount(mask)
    oxygen_reports = reports[:]
    co2_reports = reports[:]
    for bit in range(bitcount - 1, -1, -1):
        oxygen_reports = process_reports(oxygen_reports, bit, False)
        co2_reports = process_reports(co2_reports, bit, True)

    print("Part 2: The life support rating of the submarine is {}", oxygen_reports[0] * co2_reports[0])

print('---TEST---')
part1(test_input.split('\n'))
part2(test_input.split('\n'))
with open('input.txt') as f:
    print('---INPUT---')
    input = [s.strip() for s in f.readlines()]
    part1(input)
    part2(input)