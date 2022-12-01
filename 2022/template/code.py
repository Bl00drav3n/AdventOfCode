test_input = ''''''

def part1(input):
    print("Part 1: ".format())

def part2(input):
    print("Part 2:".format())

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)