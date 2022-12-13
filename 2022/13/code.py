test_input = '''
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''

def compare_integers(left, right):
    if left < right:
        return -1
    if left > right:
        return 1
    return 0

def compare_lists(left, right):
    if isinstance(left, list) or isinstance(right, list):
        if not isinstance(left, list):
            left = [left]
        elif not isinstance(right, list):
            right = [right]
        for i in range(len(left)):
            if i == len(right):
                return 1
            a = left[i]
            b = right[i]
            test = compare_lists(a, b)
            if test < 0 or test > 0:
                return test
        return -1 if len(left) < len(right) else 0
    else:
        return compare_integers(left, right)
    
def part1(input):
    if input:
        s = 0
        for i, pair in enumerate(input.strip().split('\n\n')):
            pair = pair.split()
            left = eval(pair[0])
            right = eval(pair[1])
            if compare_lists(left, right) < 0:
                s += i + 1
        print("Part 1: {}".format(s))

def part2(input):    
    if input:
        decoder_packets = [[[2]], [[6]]]
        ordered_packets = [] + decoder_packets
        for packet in [eval(line) for line in input.strip().split('\n') if line]:
            found = False
            for i, other in enumerate(ordered_packets):
                if compare_lists(packet, other) < 0:
                    ordered_packets.insert(i, packet)
                    found = True
                    break
            if not found:
                ordered_packets.append(packet)
        locations = [index + 1 for (index, packet) in enumerate(ordered_packets) if packet in decoder_packets]
        print("Part 2: {}".format(locations[0] * locations[1]))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)