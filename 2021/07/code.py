test_input = '16,1,2,0,4,2,7,1,2,14'

def actual_fuel_cost(n):
    return n * (n + 1) // 2

def index_of_minimum(values):
    return min(range(len(values)), key=values.__getitem__)

def get_fuel_costs(input, fn):
    # NOTE(rav3n): Brute force is the easy way
    positions = [int(v) for v in input.split(',')]
    minP, maxP = min(positions), max(positions)
    fuel_costs = [sum([fn(abs(src - dst)) for src in positions]) for dst in range(minP, maxP + 1)]
    return fuel_costs

def part1(input):
    fuel_costs = get_fuel_costs(input, lambda x: x)
    print("Part1: The crabs must spend {} fuel to align to the optimal position.".format(min(fuel_costs)))

def part2(input):
    fuel_costs = get_fuel_costs(input, actual_fuel_cost)
    print("Part2: The crabs must spend {} fuel to align to the optimal position.".format(min(fuel_costs)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)