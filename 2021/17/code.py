test_input = '''target area: x=20..30, y=-10..-5'''

def get_bounds(s):
    return [int(v) for v in s.split('=')[1].split('..')]

def find_solutions(input):
    xstr, ystr = input.strip().replace('target area: ', '').split(', ')
    bounds_x, bounds_y = get_bounds(xstr), get_bounds(ystr)
    solutions = set()
    # Bruteforce, idc. We assume that the target x position is always to the right and
    # the target y position is always below the starting point (0,0).
    for i in range(0, bounds_x[1] + 1):
        for j in range(bounds_y[0], bounds_x[1] + 1):
            x = 0
            y = 0
            ymax = 0
            vx = i
            vy = j
            while True:
                x += vx
                vx = vx - 1 if vx > 0 else 0
                y += vy
                ymax = max(ymax, y)
                vy -= 1
                if x >= bounds_x[0] and x <= bounds_x[1] and y >= bounds_y[0] and y <= bounds_y[1]:
                    solutions.add((i, j, ymax))
                    break
                if x > bounds_x[1] or y < bounds_y[0]:
                    break
    return solutions

def part1(input):
    solutions = find_solutions(input)
    print("Part 1: The highest reachable y position is {}".format(max(solutions, key=lambda item: item[1])[2]))

def part2(input):
    solutions = find_solutions(input)
    print("Part 2: There are {} distinct initial velocities that cause the probe to be withing the target area at any step".format(len(solutions)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)