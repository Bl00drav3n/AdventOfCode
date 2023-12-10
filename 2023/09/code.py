test_input = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''

def extrapolate(s) -> list[int]:
    # The extrapolated value is just the sum of all the last values after each reduction step
    values = []
    while any(s):
        values.append(s[-1])
        s = ([t[1] - t[0] for t in zip(s, s[1:])])
    return sum(values)

def read_series(input) -> list[list[int]]:
    return [[int(n) for n in line.split(' ')] for line in input.strip().split('\n')]

def part1(input):
    values = [extrapolate(s) for s in read_series(input)]
    print("Part 1: The sum of extrapolated values is {}".format(sum(values)))

def part2(input):
    # To extrapolate to the left, simply reverse the list and use the same algorithm
    values = [extrapolate(s[::-1]) for s in read_series(input)]
    print("Part 2: The sum of extrapolated values is {}".format(sum(values)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)