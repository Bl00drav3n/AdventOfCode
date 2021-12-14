test_input = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''

def read_input(input):
    template, rules = input.strip().split('\n\n')
    rules = {r[0]:r[1] for r in [rule.split(' -> ')for rule in rules.split('\n')]}
    return template, rules

def add_pair_counts(a, b):
    tmp = dict(a)
    for k, v in b.items():
        if not k in tmp:
            tmp[k] = 0
        tmp[k] += v
    return tmp

def update(counts, rules):
    tmp = {}
    for k, v in counts.items():
        # When we have x instances of pattern AC with rule AC -> B, 
        # then the result will be x instances of AB and x instances of BC
        a, b = rules[k]
        if not a in tmp:
            tmp[a] = 0
        if not b in tmp:
            tmp[b] = 0
        tmp[a] += v
        tmp[b] += v
    return tmp

def count_pairs(template, rules, n):
    total_pair_counts = {}
    # Map every rule to the 2 different patterns
    rules = {k:(k[0] + v, v + k[1]) for k,v in rules.items()}
    # For every pair appearing in the template, iteratively apply the rules and count the number of pairs
    for i in range(len(template) - 1):
        pair_counts = {k:0 for k in rules.keys()}
        pair_counts[template[i:i+2]] = 1
        for j in range(n):
            pair_counts = update(pair_counts, rules)
        total_pair_counts = add_pair_counts(total_pair_counts, pair_counts)
    return total_pair_counts

def count_elements(template, rules, n):
    # Count how many times any pair appears after n iterations
    total_pair_counts = count_pairs(template, rules, n)

    # Count the number of appearances of any element
    elements = {}
    for k in total_pair_counts.keys():
        for c in k:
            if not c in elements:
                elements[c] = 0
            elements[c] += total_pair_counts[k]

    # Each element is counted twice, except the first and last one, compensate for that
    elements[template[0]] += 1
    elements[template[-1]] += 1
    elements = {k:v//2 for k,v in elements.items()}
    return elements

def part1(input):
    template, rules = read_input(input)
    counts = sorted(count_elements(template, rules, 10).values())
    print("Part 1: The difference between the quantity of the most common and the least common element is {}".format(counts[-1] - counts[0]))

def part2(input):
    template, rules = read_input(input)
    counts = sorted(count_elements(template, rules, 40).values())
    print("Part 2: The difference between the quantity of the most common and the least common element is {}".format(counts[-1] - counts[0]))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)