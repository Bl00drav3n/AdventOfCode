test_input = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''

import string

def parse(input):
    # Find first and last digit for each line, return 10*First+Last as int
    return list(map(lambda x: 10 * int(x[0]) + int(x[-1]) if x else 0, ["".join(filter(lambda x: x in string.digits, line)) for line in input.split('\n')]))

def find_text_digits(digits, text):
    # Using text encoding for the digits, record all digit occurences as a tuple of position, ascii value and text encoding and return as list
    lst = []
    for k, v in digits.items():
        pos = 0
        while True:
            pos = text.find(k,pos)
            if pos == -1:
                break
            lst.append((pos, v, k))
            pos += len(k)
    return lst

def convert(line):
    # Replace text encoding of digits with their ascii value from left to right, handling overlaps
    digit_map = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
    text_digits = sorted(find_text_digits(digit_map, line), key=lambda x: x[0])
    result = line
    if text_digits:
        result = ""
        cursor = 0
        for pos, v, k in text_digits:
            cursor = min(cursor, pos)
            result += line[cursor:pos] + v
            cursor = pos + len(k)
        result += line[cursor:]
    return result

def part1(input):
    print("Part 1: The sum of calibration values is {}".format(sum(parse(input))))

def part2(input):
    input = "\n".join([convert(line) for line in input.split('\n')])
    print("Part 2: The sum of calibration values is {}".format(sum(parse(input))))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)