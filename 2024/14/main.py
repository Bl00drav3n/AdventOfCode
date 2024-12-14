test_input = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''

def read_input(input):
    robots = []
    for line in input.strip().split('\n'):
        robots.append([[int(i) for i in vec] for vec in [item.split('=')[1].split(',') for item in line.split(' ')]])
    return robots

def update(robots, width, height):
    for robot in robots:
        robot[0][0] = (robot[0][0] + robot[1][0]) % width
        robot[0][1] = (robot[0][1] + robot[1][1]) % height

def check_quadrants(robots, width, height):
    quadrants = [0, 0, 0, 0]
    half_width = width // 2
    half_height = height // 2
    for robot in robots:
        x, y = robot[0]
        if not (x == half_width or y == half_height):
            qx = x // (half_width + 1)
            qy = y // (half_height + 1)
            assert qx in (0, 1) and qy in (0, 1), "Invalid quadrant!"
            quadrants[2 * qy + qx] += 1
    return quadrants

def correlation(robots):
    corr = 0
    for robot in robots:
        x, y = robot[0]
        for other_robot in robots:
            ox, oy = other_robot[0]
            cx = x - ox
            cy = y - oy
            corr += cx * cx + cy * cy
    return corr

def part1(input, iterations, width, height):
    robots = read_input(input)
    for _ in range(iterations): update(robots, width, height)
    quadrants = check_quadrants(robots, width, height)
    safety_factor = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
    print("Part 1: The safety factor is {}.".format(safety_factor))

def part2(input, width, height):
    # The idea is that a pattern like a christmas tree should be highly spatially correlated, so we define a
    # (dumb) correlation function and everytime the correlation value is smaller than the previous, we output
    # the pattern to a file. The iteration counter can also be read out from the result file.
    with open('out.txt', 'w') as file:
        max_iterations = 10000
        robots = read_input(input)
        corr = 10e300
        for i in range(max_iterations):
            if i % 100 == 0:
                print("ITERATION {}".format(i + 1))
            update(robots, width, height)
            test_corr = correlation(robots)
            if test_corr < corr:
                corr = test_corr
                print("Candidate on iteration {}, correlation {}".format(i + 1, corr))
                buffer = [None] * height
                for y in range(height): buffer[y] = ['.'] * width
                for robot in robots:
                    buffer[robot[0][1]][robot[0][0]] = '#'
                file.write('ITERATION {}:\n'.format(i))
                for line in buffer:
                    file.write(''.join(line) + '\n')
                file.write('\n')
                file.flush()

print('---TEST---')
part1(test_input, 100, 11, 7)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input, 100, 101, 103)
    part2(input, 101, 103)