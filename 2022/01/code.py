test_input = '''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000'''

def snax(input):
    return sorted([sum([int(calories) for calories in elf.split('\n')]) for elf in [elfs for elfs in input.split('\n\n')]],reverse=True)

def part1(input):
    result = snax(input)[0]
    print("Part 1: {}".format(result))

def part2(input):
    result = sum(snax(input)[:3])
    print("Part 2: {}".format(result))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)