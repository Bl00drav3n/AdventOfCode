test_input = '3,4,3,1,2'

def breed_feesh(input, days):
    # We only have to keep track of the total number of feesh corresponding to their internal timer
    counts = [0] * 9
    for feesh in [int(v) for v in input.split(',')]:
        counts[feesh] += 1
    for i in range(0, days):
        zero = counts[0]
        counts = [*counts[1:], zero]
        counts[6] += zero
    return sum(counts)

def part1(input):
    days = 80
    count = breed_feesh(input, days)
    print('Part 1: After {} days, there would be a total of {} feesh.'.format(days, count))

def part2(input):
    days = 256
    count = breed_feesh(input, days)
    print('Part 2: After {} days, there would be a total of {} feesh.'.format(days, count))
    
print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.readline()
    print('---INPUT---')
    part1(input)
    part2(input)