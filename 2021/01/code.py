import functools
test_input = '''199
200
208
210
200
207
240
269
260
263'''

def count_positive_differences(measurements):
    differences = [m[1] - m[0] for m in zip(measurements, measurements[1:])]
    return sum([1 for d in differences if d > 0 ])

def part1(input):
    depth_measurements = [int(entry) for entry in input]
    print("Part 1: There are {} measurements that are larger than the previous measurements.".format(count_positive_differences(depth_measurements)))

def part2(input):
    depth_measurements = [int(entry) for entry in input]
    sliding_window_sums = [m[0] + m[1] + m[2] for m in zip(depth_measurements, depth_measurements[1:], depth_measurements[2:])]
    print("Part 2: There are {} sums that are larger than the previous sums.".format(count_positive_differences(sliding_window_sums)))

print("--- TEST ---")
part1(test_input.split('\n'))
part2(test_input.split('\n'))

with open('input.txt') as f:    
    print("\n--- INPUT ---")
    input = f.readlines()
    part1(input)
    part2(input)