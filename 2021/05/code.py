import time

test_input = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2'''

def read_input(input):
    lines = input.split('\n')
    segments = [[entry[0].split(','), entry[2].split(',')] for entry in [line.split() for line in lines if line]]
    segments = [[[int(s[0][0]), int(s[0][1])],[int(s[1][0]), int(s[1][1])]] for s in segments]
    return segments

def create_field(segments):
    minx = segments[0][0][0]
    miny = segments[0][0][1]
    maxx = minx
    maxy = miny
    for seg in segments:
        for point in seg:
            minx = min(point[0], minx)
            maxx = max(point[0], maxx)
            miny = min(point[1], miny)
            maxy = max(point[1], maxy)
    return [[0 for x in range(0, maxx + 1)] for y in range(0, maxy + 1)]

def get_endpoints_ordered(segment, axis):
    a, b = segment[0][axis], segment[1][axis]
    return (a, b) if a < b else (b, a)

def is_diagonal(s):
    return s[0][0] != s[1][0] and s[0][1] != s[1][1]

def add_segments_hv(points, segments):
    # NOTE(rav3n): Just brute force it, because the size fits into memory
    for s in segments:
        if s[0][0] != s[1][0]:
            y = s[0][1]
            a, b = get_endpoints_ordered(s, 0)
            for x in range(a, b + 1):
                points[y][x] += 1
        else:
            x = s[0][0]
            a, b = get_endpoints_ordered(s, 1)
            for y in range(a, b + 1):
                points[y][x] += 1
    return points

def add_segments_diag(points, segments):
    # NOTE(rav3n): Too tired to make this look nice
    for s in segments:
        P, Q = s[0], s[1]
        if P[0] < Q[0]:
            if P[1] < Q[1]:
                # P
                #  Q
                for i in range(Q[0] - P[0] + 1):
                    points[(P[1] + i)][P[0] + i] += 1
            else:
                #  Q
                # P
                for i in range(Q[0] - P[0] + 1):
                    points[(P[1] - i)][P[0] + i] += 1
        else:
            if P[1] < Q[1]:
                #  P
                # Q
                for i in range(P[0] - Q[0] + 1):
                    points[(P[1] + i)][P[0] - i] += 1
            else:
                # Q
                #  P
                for i in range(P[0] - Q[0] + 1):
                    points[(P[1] - i)][P[0] - i] += 1
    return points

def get_overlap_count(points):
    return sum([len([v for v in row if v > 1]) for row in points])

def print_points(points):
    [print(''.join([str(v) if v else '.' for v in row])) for row in points]

def part1(input):
    ts1 = time.time_ns()
    segments_hv = [s for s in read_input(input) if not is_diagonal(s)]
    points = add_segments_hv(create_field(segments_hv), segments_hv)
    ts2 = time.time_ns()
    dt = (ts2 - ts1) / 1e6
    print('Part 1: The number of points where at least two lines overlap is {} ({}ms)'.format(get_overlap_count(points), dt if dt >= 1 else "<1"))

def part2(input):
    ts1 = time.time_ns()
    segments_hv = [s for s in read_input(input) if not is_diagonal(s)]
    segments_diag = [s for s in read_input(input) if is_diagonal(s)] 
    points = add_segments_hv(create_field(segments_hv), segments_hv)
    points = add_segments_diag(points, segments_diag)
    ts2 = time.time_ns()
    dt = (ts2 - ts1) / 1e6
    print('Part 2: The number of points where at least two lines overlap is {} ({}ms)'.format(get_overlap_count(points), dt if dt >= 1 else "<1"))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)