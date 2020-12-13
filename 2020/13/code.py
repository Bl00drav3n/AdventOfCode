import math

test_input = '''939
7,13,x,x,59,x,31,19'''

def get_bus_lines(input):
    return [int(id) for id in input[1].split(',') if id != 'x']

def get_earliest_departure_time(input):
    return int(input[0])

def get_answer_part1(input):
    input = input.splitlines()
    arrival = get_earliest_departure_time(input)
    bus_lines = get_bus_lines(input)
    wait_times = [(id - (arrival % id), id) for id in bus_lines]
    optimal = min(wait_times, key = lambda x: x[0])
    return optimal[0] * optimal[1]

def get_answer_part2(input):
    input = input.splitlines()
    arrival = get_earliest_departure_time(input)
    bus_lines = get_bus_lines(input)


print('Answer part1 (TEST):', get_answer_part1(test_input))
with open('input.txt') as file:
    input = file.read()
    print('Answer part1:', get_answer_part1(input))

'''
--> Part2?
t = p * n
t + c = q * m => t = q * m - c
p * n = q * m - c
q * m - p * n = c
q * m = c mod p
'''