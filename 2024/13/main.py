import re
import math

test_input = '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''

def configuration(game):
    string_a, string_b, string_prize = game.split('\n')
    button_expr = "[XY]\+\d+"
    prize_expr = "[XY]=\d+"
    A = (int(expr.split('+')[1]) for expr in re.findall(button_expr, string_a))
    B = (int(expr.split('+')[1]) for expr in re.findall(button_expr, string_b))
    P = (int(expr.split('=')[1]) for expr in re.findall(prize_expr, string_prize))
    return A, B, P

def modify(configuration):
    A, B, P = configuration
    px, py = P
    return A, B, (10000000000000 + px, 10000000000000 + py)

def solve(configuration):
    A, B, P = configuration
    ax, ay = A
    bx, by = B
    px, py = P
    result = 0

    # Powered by chatgpt-4o
    # ---PROMPT---
    # Suppose you are given the system of diophantine equations in 2 variables 
    # px = ax * a + bx * b and py = ay * a + by * b, with known values for px, py, ax and bx. 
    # How do you solve these for integers a and b?
    # ------------

    # Solve by inverting the matrix (if invertible aka non-singular) and check for integer solutions
    d = ax * by - bx * ay
    if d != 0:
        a = divmod(by * px - bx * py, d)
        b = divmod(ax * py - ay * px, d)
        if a[1] == 0 and b[1] == 0:
            # Remainders are 0, hence we got an integer solution
            result = 3 * a[0] + b[0]
    else:
        # If the equations are consistent, I suppose one can just solve either of the 1D diophantine equations.
        assert False, "Not implemented!"
    return result

def part1(input):
    tokens = sum([solve(configuration(game)) for game in input.strip().split('\n\n')])
    print("Part 1: The fewest tokens you would have to spend is {}.".format(tokens))

def part2(input):
    tokens = sum([solve(modify(configuration(game))) for game in input.strip().split('\n\n')])
    print("Part 2: The fewest tokens you would have to spend is {}.".format(tokens))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)