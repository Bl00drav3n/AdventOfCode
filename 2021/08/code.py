test_input = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'''

segments = {
    'abcefg'  : '0', #6
    'cf'      : '1', #2
    'acdeg'   : '2', #5
    'acdfg'   : '3', #5
    'bcdf'    : '4', #4
    'abdfg'   : '5', #5
    'abdefg'  : '6', #6
    'acf'     : '7', #3
    'abcdefg' : '8', #7
    'abcdfg'  : '9'  #6
}

def is_unique(pattern):
    return len(pattern) in (2, 3, 4, 7)

def read_input(input):
    return [[entry.strip() for entry in line.split('|')] for line in input.split('\n') if line]

def get_unique_patterns(lines):
    return [[''.join(sorted(pattern)) for pattern in line.split() if is_unique(pattern)] for line in lines]

def add(a, b):
    return ''.join(sorted(set(a).union(set(b))))

def subtract(a, b):
    return ''.join(sorted(set(a) - set(b)))

def find_segment_a(m):
    # Pattern of length 3 (7) minus pattern of length 2 (1) is segment a
    return subtract(m[3][0], m[2][0])

def find_segment_g(m):
    # Mask is pattern of length 4 (4) plus pattern of length 3 (7)
    # Subtracting the mask from each pattern of length 6 and filtering for the leftover item of length 1 returns segment g
    patterns = [subtract(pattern, add(m[4][0], m[3][0])) for pattern in m[6]]
    return [p for p in patterns if len(p) == 1][0]

def find_segment_e(m):
    # We know how to find segment g, so to find segment e, remove the patterns of 4 and 7 from 8 and also remove segment g
    return subtract(subtract(subtract(m[7][0], m[3][0]), m[4][0]), find_segment_g(m))

def find_segment_d(m):
    # With segments e and g found, we create a mask with the pattern of 7 plus the segments e and g.
    # Subtracting the mask from each pattern of length 5 and filtering for the item of length 1 returns segment d
    mask = add(m[3][0], find_segment_e(m) + find_segment_g(m))
    patterns = [subtract(item, mask) for item in m[5]]
    return [item for item in patterns if len(item) == 1][0]

def find_segment_b(m):
    # With segment d found, we subtract the pattern of 1 from 4 and remove segment d, to return segment b
    return subtract(subtract(m[4][0], m[2][0]), find_segment_d(m))

def find_segment_f(m, s):
    # To find segment f, we need the segments a, b, d, e and g - adding them together creates a mask.
    # This mask is subtracted from all patterns of length 6 and filtered for the item of length 1, which returns segment f
    s = {value:key for key, value in s.items()}
    mask = s['a']+s['b']+s['d']+s['e']+s['g']
    patterns = [subtract(p, mask) for p in m[6]]
    return [p for p in patterns if len(p) == 1][0]

def find_segment_c(m, s):
    # With segment f found, we simply need to remove segment f from the pattern of 1
    s = {value:key for key, value in s.items()}
    return subtract(m[2][0], s['f'])

def convert(pattern, segment_list, segments):
    # Map the segment wires to the actual segments and lookup the pattern in the segment table to find the displayed digit
    key = ''.join(sorted([segment_list[p] for p in pattern]))
    return segments[key]

def part1(input):
    lines = read_input(input)
    unique_count = sum([len(patterns) for patterns in get_unique_patterns([line[1] for line in lines])])
    print("Part 1: The digits 1, 4, 7 and 8 appear {} times".format(unique_count))

def part2(input):
    test = add(add('fdcge', 'fecdb'), 'fabcd')
    lines = read_input(input)
    pattern_list = [[''.join(sorted(item)) for item in line[0].split()] for line in lines]
    value_list = [[''.join(sorted(item)) for item in line[1].split()] for line in lines]
    total = 0
    for i, item in enumerate(pattern_list):
        segment_map = {}
        pattern_len_map = {2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        for pattern in item:
            pattern_len_map[len(pattern)].append(pattern)
        # Reverse the cipher
        segment_map[find_segment_a(pattern_len_map)] = 'a'
        segment_map[find_segment_g(pattern_len_map)] = 'g'
        segment_map[find_segment_e(pattern_len_map)] = 'e'
        segment_map[find_segment_d(pattern_len_map)] = 'd'
        segment_map[find_segment_b(pattern_len_map)] = 'b'
        segment_map[find_segment_f(pattern_len_map, segment_map)] = 'f'
        segment_map[find_segment_c(pattern_len_map, segment_map)] = 'c'
        # Convert the output value
        value = int(''.join([convert(pattern, segment_map, segments) for pattern in value_list[i]]))
        total += value
    print("Part 2: The sum of all output values is {}".format(total))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)