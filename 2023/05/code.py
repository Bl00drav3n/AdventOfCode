test_input = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''

def read_input(input):
    # Return seeds as list of int, name_mappings as dict of string -> string, range_mappings as dict of string -> list of list of integers (dst, src, len)
    blocks = input.strip().split('\n\n')
    seeds = list(map(int, blocks[0].split(':')[1].strip().split(' ')))
    name_mappings = {}
    range_mappings = {}
    for block in blocks[1:]:
        lines = block.split('\n')
        header = lines[0].split(' ')[0].split('-')
        lhs = header[0]
        rhs = header[2]
        name_mappings[lhs] = rhs
        lines = lines[1:]
        range_mappings[lhs] = [list(map(int, line.split(' '))) for line in lines]
    return seeds, name_mappings, range_mappings

def match_range(mapping, rstart, rend, result, ranges):
    # Try to find overlaps of range defined by rstart and rend with mappings in mapping
    # Updates the result list with mapped ranges and ranges list with yet to be processed new ranges
    for m in mapping:
        mstart = m[1]
        mlen = m[2]
        mend = mstart + mlen - 1
        # Differentiate 
        if rstart >= mstart and rstart <= mend and rend >= mstart and rend <= mend:
            # fully contained [mmmmmmmm]
            result.append([rstart + m[0] - mstart, rend - rstart + 1])
            return True
        elif rstart <= mstart and rend >= mstart and rend <= mend:
            # left overlap [.....mmm]
            ranges.append([rstart, mstart - rstart])
            result.append([m[0], rend - mstart + 1])
            return True
        elif rstart >= mstart and rstart <= mend and rend >= mend:
            # right overlap [mmm.....]
            ranges.append([mend + 1, rend - mend])
            result.append([rstart + m[0] - mstart, mend - rstart + 1])
            return True
        elif rstart <= mstart and rend >= mend:
            # overcovered [..mmm...]
            # split into a nonmapped range and a right overlap
            result.append([rstart, mstart - rstart])
            ranges.append([mstart, rend - mstart + 1])
            return True
    return False

def map_ranges(ranges, mapping):
    # Algorithm to map input ranges to corresponding output ranges, depending on overlaps with ranges defined in mapping
    # Return mapped ranges as list of list of integers (start, len)
    result = []
    while ranges:
        r = ranges.pop()
        rstart = r[0]
        rlen = r[1]
        rend = rstart + rlen - 1
        if not match_range(mapping, rstart, rend, result, ranges):
            # No overlap was found, corresponds to 1:1 mapping
            result.append(r)
    return result

def seed_range_to_location_range(seed_range, name_map, range_map):
    s = 'seed'
    r = [seed_range]
    while s != 'location':
        r = map_ranges(r, range_map[s])
        s = name_map[s]
    return r

def minimum_location_for_range(r, name_map, range_map):
    return min([r[0] for r in seed_range_to_location_range(r, name_map, range_map)])

def part1(input):
    seeds, name_map, range_map = read_input(input)
    # interpret seeds as single units with range 1
    locations = [minimum_location_for_range([seed, 1], name_map, range_map) for seed in seeds]
    print("Part 1: The lowest location number is {}".format(min(locations)))

def part2(input):
    seeds, name_map, range_map = read_input(input)
    ranges = zip(seeds[::2], seeds[1::2])
    locations = [minimum_location_for_range(r, name_map, range_map) for r in ranges]
    print("Part 2: The lowest location number is {}".format(min(locations)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)