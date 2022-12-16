test_input = '''
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def read_input(input):
    sensors = {}
    for row in input.strip().split('\n'):
        sensor_str, beacon_str = row.split(': ')
        sxstr, systr = sensor_str[10:].split(', ')
        bxstr, bystr = beacon_str[21:].split(', ')
        sensor = (int(sxstr.split('=')[1]), int(systr.split('=')[1]))
        beacon = (int(bxstr.split('=')[1]), int(bystr.split('=')[1]))
        sensors[sensor] = distance(sensor, beacon)
    return sensors

def find_intervals_on_axis(sensors, axis, test):
    intervals = []
    for sensor, distance in sensors.items():
        dy = abs(test - sensor[axis])
        if dy <= distance:
            dx = distance - dy
            intervals.append((sensor[1 - axis] - dx, sensor[1 - axis] + dx))
    return intervals

def overlapping(a, b):
    return a[0] >= b[0] - 1 and a[0] <= b[1] + 1 or b[0] >= a[0] - 1 and b[0] <= a[1] + 1

def merge(a, b):
    return (min(a[0], b[0]), max(a[1],b[1]))

def simplify(intervals):
    while len(intervals) > 1:
        test_interval = intervals.pop()
        for i in range(len(intervals)):
            if overlapping(test_interval, intervals[i]):
                other = intervals.pop(i)
                new_interval = merge(test_interval, other)
                intervals.append(new_interval)
                test_interval = None
                break
        if test_interval:
            intervals.append(test_interval)
            return

def covers(intervals, left, right):
    simplify(intervals)
    if len(intervals) > 1:
        return False
    else:
        return left >= intervals[0][0] or right <= intervals[0][1]

def part1(input, test_y):
    if input:
        sensors = read_input(input)
        intervals = find_intervals_on_axis(sensors, 1, test_y)
        simplify(intervals)
        print("Part 1: {}".format(sum(map(lambda x: x[1] - x[0], intervals))))

import time
def part2(input, max_dim):
    if input:
        start = time.perf_counter_ns()
        sensors = read_input(input)
        p = [0, 0]
        for axis in [0, 1]:
            # NOTE: People that are not lazy would determine the bounding boxes for each sensor and restrict the search area
            # Luckily I am lazy and will just slack. :)
            for i in range(max_dim + 1):
                interval = find_intervals_on_axis(sensors, axis, i)
                if not covers(interval, 0, max_dim):
                    p[axis] = i
                    break
        print("Part 2: {}".format(4000000 * p[0] + p[1]))
        end = time.perf_counter_ns()
        print("Time spent: {} sec".format(int((end - start) / 1e9)))

print('---TEST---')
part1(test_input, 10)
part2(test_input, 20)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input, 2000000)
    part2(input, 4000000)