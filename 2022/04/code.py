test_input = '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''

def contained(pair):
    return (pair[1][0] >= pair[0][0] and pair[1][1] <= pair[0][1]) or (pair[0][0] >= pair[1][0] and pair[0][1] <= pair[1][1])

def overlapping(pair):
    return (pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][0]) or (pair[0][0] <= pair[1][1] and pair[0][1] >= pair[1][1]) or contained(pair)

def parse_input(input, filter_func):
    pairs = map(lambda sections: (tuple(map(int, sections[0].split('-'))), tuple(map(int, sections[1].split('-')))), map(lambda line: line.split(','), input.strip().split('\n')))
    return filter(filter_func, pairs)

def part1(input):
    pairs = list(parse_input(input, contained))
    print("Part 1: {}".format(len(pairs)))

def part2(input):
    pairs = list(parse_input(input, overlapping))
    print("Part 2: {}".format(len(pairs)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)