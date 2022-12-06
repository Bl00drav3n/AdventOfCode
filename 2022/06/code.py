test_input = '''mjqjpqmgbljsphdztnvjfqwrcgsmlb'''

def test_start(window):
    return len(set(window)) == 4

def test_msg(window):
    return len(set(window)) == 14

def test(input, test_fn, window_size):
    for i in range(0, len(input) - window_size):
        window = input[i:i+window_size]
        if test_fn(window):
            return i + window_size

def part1(input):
    first = test(input, test_start, 4)
    print("Part 1: {}".format(first))

def part2(input):
    first = test(input, test_msg, 14)
    print("Part 2: {}".format(first))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)