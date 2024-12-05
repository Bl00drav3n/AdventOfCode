test_input = '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''

def read_input(input):
    rules, updates = input.strip().split("\n\n")
    rule_table = {}
    for rule in rules.split("\n"):
        parse_rule(rule_table, rule)

    # convert page updates to lists of integers
    updates = [[int(page) for page in pages.split(',')] for pages in [update for update in updates.split('\n')]]

    return rule_table, updates

def parse_rule(rules, rule):
    lhs, rhs = [int(x) for x in rule.split("|")]
    if not lhs in rules:
        rules[lhs] = set()
    if not rhs in rules:
        rules[rhs] = set()
    rules[lhs].add(rhs)

def verify(rules, update):
    for i in range(len(update)):
        index = len(update) - i - 1
        page = update[index]
        for j in range(index):
            if update[j] in rules[page]:
                return False
    return True

def check_updates(rule_table, updates):
    correct_updates = []
    incorrect_updates = []
    for update in updates:
        if verify(rule_table, update):
            correct_updates.append(update)
        else:
            incorrect_updates.append(update)
    return correct_updates, incorrect_updates

def repair(rule_table, corrupted):
    # Didn't verify that it always works, but it does work for my input
    # There might be input sets where you need to do a recursion, for example
    # when there is a rule like: A < B < C and you want to insert A, but only C is in
    # the stream already. It would in this case add A to the end of the stream, because it does
    # not check for all of A's dependencies.
    result = []
    for page in corrupted:
        inserted = False
        for i in range(len(result)):
            if result[i] in rule_table[page]:
                result.insert(i, page)
                inserted = True
                break
        if not inserted:
            result.append(page)

    assert verify(rule_table, result), "Validation failed!"

    return result

def get_middle_page_numbers(updates):
    return [update[len(update) // 2] for update in updates]

def part1(input):
    rule_table, updates = read_input(input)
    correct_updates, _ = check_updates(rule_table, updates)
    middle_page_numbers = get_middle_page_numbers(correct_updates)

    print("Part 1: The sum of the middle page number from the correctly-ordered upates is {}.".format(sum(middle_page_numbers)))

def part2(input):
    rule_table, updates = read_input(input)
    _, incorrect_updates = check_updates(rule_table, updates)
    corrected_updates = [repair(rule_table, update) for update in incorrect_updates]
    middle_page_numbers = get_middle_page_numbers(corrected_updates)

    print("Part 2: The sum of the middle page number from the corrected updates is {}".format(sum(middle_page_numbers)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)