test_inputs = ['0,3,6', '1,3,2', '2,1,3', '1,2,3', '2,3,1', '3,2,1', '3,1,2']
input_part1 = '2,20,0,4,1,17'

def speak_number(numbers, turn, n):
    result = 0
    if n in numbers:
        result = turn - numbers[n]
    numbers[n] = turn
    return result

def play(input, n):
    starting_numbers = input.split(',')
    spoken_numbers = {}
    for turn, number in enumerate(starting_numbers[:-1]):
        spoken_numbers[int(number)] = turn
    last = int(starting_numbers[-1])
    for turn in range(len(starting_numbers) - 1, n - 1):
        last = speak_number(spoken_numbers, turn, last)
    return last

[print('2020th number (TEST): {} -> {}'.format(input, play(input, 2020))) for input in test_inputs]
print('2020th number: {} -> {}'.format(input_part1, play(input_part1, 2020)))

[print('30000000th number (TEST): {} -> {}'.format(input, play(input, 30000000))) for input in test_inputs]
print('30000000th number: {} -> {}'.format(input_part1, play(input_part1, 30000000)))