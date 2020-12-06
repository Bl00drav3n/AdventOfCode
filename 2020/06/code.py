import functools

test_input = '''abc

a
b
c

ab
ac

a
a
a
a

b
'''

def get_groups(input):
    return [group.strip() for group in input.split('\n\n')]

def get_positive_answers(group):
    return [[answer for answer in answers] for answers in group.splitlines()]

def get_sum_of_positive_answers_part1(input):
    count = 0
    for group in get_groups(input):
        positive_answers = []
        [[positive_answers.append(answer) for answer in answers] for answers in get_positive_answers(group)]
        count += len(set(positive_answers))
    return count

def get_sum_of_positive_answers_part2(input):
    count = 0
    for group in get_groups(input):
        answers = [set([answer for answer in answers]) for answers in get_positive_answers(group)]
        count += len(functools.reduce(lambda x, y: x.intersection(y), answers))
    return count

print('Sum of positive answers part1 (TEST):', get_sum_of_positive_answers_part1(test_input))
print('Sum of positive answers part2 (TEST):', get_sum_of_positive_answers_part2(test_input))
with open('input.txt') as file:
    input = file.read()
    print('Sum of positive answers part1:', get_sum_of_positive_answers_part1(input))
    print('Sum of positive answers part2:', get_sum_of_positive_answers_part2(input))