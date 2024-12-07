test_input = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''

def read_input(input):
    result = []
    lines = input.strip().split('\n')
    for line in lines:
        key, values = line.split(": ")
        result.append((int(key), [int(v) for v in values.split(' ')]))
    return result

# Exhaustive search
def check_calibration(result, lst, value):
    if not lst:
        return result == value
    return check_calibration(result, lst[1:], value + lst[0]) or check_calibration(result, lst[1:], value * lst[0])

# Exhaustive search
def check_calibration2(result, lst, value):
    if not lst:
        return result == value
    return check_calibration2(result, lst[1:], value + lst[0]) or check_calibration2(result, lst[1:], value * lst[0]) or check_calibration2(result, lst[1:], int(str(value) + str(lst[0])))

def part1(input):
    data = read_input(input)
    correct_calibration_results = [value for value, lst in data if check_calibration(value, lst, 0)]
    
    print("Part 1: The total calibration result is {}.".format(sum(correct_calibration_results)))

def part2(input):
    data = read_input(input)
    correct_calibration_results = [value for value, lst in data if check_calibration2(value, lst, 0)]
    print("Part 2: The total calibration result is {}.".format(sum(correct_calibration_results)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)