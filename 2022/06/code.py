test_input = '''mjqjpqmgbljsphdztnvjfqwrcgsmlb'''

START_WINDOW_SIZE = 4
MSG_WINDOW_SIZE = 14

def test(input, window_size):
    for i in range(0, len(input) - window_size):
        window = input[i:i+window_size]
        if len(set(window)) == window_size:
            return i + window_size

def part1(input):
    first = test(input, START_WINDOW_SIZE)
    print("Part 1: {}".format(first))

def part2(input):
    first = test(input, MSG_WINDOW_SIZE)
    print("Part 2: {}".format(first))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)