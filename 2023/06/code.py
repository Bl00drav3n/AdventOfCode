test_input = '''Time:      7  15   30
Distance:  9  40  200'''

import math
import re
import functools
import operator

# We use the simple relationship s(t) = t * (t0 - t) - d, 
# with s the distance after holding the button down for t ms, t0 the time a race takes in ms, and d the record in mm.
# This traces out an upside down parabola, with s > 0 indicating that we have moved further than the distance d at the end of the race.
# Because of the negative curvature (s''(t)=-2), we know that s will be positive (or 0) between the left and right zero crossing point (if they exist).
# Solving t * (t0 - t) - d = 0 for t will yield 0, 1 or 2 real solutions, we restrict ourselves to the case where we have 2 real solutions (di > 0).
# For the smaller solution we apply ceil(), to the larger we apply floor() to get possible integer solutions. The number of integers inside the interval
# corresponds to the number of possible times t, that will result in a distance > d.
# In case the zeroes are exactly an integer, we need to adjust the range by adding/subtracting 1.
# When there is only one distinct real zero, then there is no possible way to break the record, as well as when there are only complex solutions.
# NOTE: It's possible, that the graph is positioned in such a way, that the zeroes lie exactly between two integers, in which case we would return 0, True.
# This case did not happen for me, so it was ignored.

def solve(t, d):
    # Solve for the zeroes of the quadratic t0 * (t - t0) = d
    # Return the length of the integer interval defined by the 2 solutions + 1, as well as a boolean that indicates whether we have a real solution
    di = t*t/4 - d
    if di > 0:
        t1 = int(math.ceil(t/2 - math.sqrt(di)))
        t2 = int(math.floor(t/2 + math.sqrt(di)))
        if t1 * (t - t1) == d:
            t1 += 1
        if t2 * (t - t2) == d:
            t2 -= 1
        return t2 - t1 + 1, True
    else:
        return 0, False
    
def part1(input):
    time, distance = input.strip().split('\n')
    f = lambda x: re.findall('\d+', x)
    time = [int(s) for s in f(time)]
    distance = [int(s) for s in f(distance)]
    result = [s for (s, real) in [solve(t, d) for (t, d) in zip(time, distance)] if real]
    print("Part 1: The product of the numbers is {}".format(functools.reduce(operator.mul, result)))

def part2(input):
    time, distance = input.strip().split('\n')
    f = lambda x: re.findall('\d+', x.replace(' ', ''))
    time = int(f(time)[0])
    distance = int(f(distance)[0])
    result, real = solve(time, distance)
    print("Part 2: There are {} ways to beat the record".format(result if real else 0))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)