test_input_part1 = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
'''

test_input_part2 = '''shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
'''

def parse_rhs(child):
    is_digit = lambda c: c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    tokens = child.split(' ')
    result = None
    if is_digit(tokens[0]):
        result = (' '.join(tokens[1:3]), int(tokens[0]))
    elif tokens[0] == 'no':
        pass
    else:
        print("Error parsing child:", child)
    return result

def parse_input(input):
    bags = {}
    for input in input.splitlines():
        lhs, rhs = tuple(input.split(" contain "))
        rhs_children = rhs.split(', ')
        children = [parse_rhs(child) for child in rhs_children]
        key = " ".join(lhs.split(' ')[:2])
        bags[key] = children
    return bags

def contains(bags, color, needle):
    for child in bags[color]:
        if child:
            child_color = child[0]
            if child_color == needle or contains(bags, child_color, needle):
                return True
    return False

def number_of_bags(bags, color):
    count = 1
    for child in bags[color]:
        if child:
            child_color = child[0]
            child_count = child[1]
            count += child_count * number_of_bags(bags, child_color)
    return count

def get_number_of_colors(input):
    bags = parse_input(input)
    needle = 'shiny gold'
    return sum([1 if color != needle and contains(bags, color, needle) else 0 for color in bags.keys()])

def get_number_of_contained_bags(input):
    return number_of_bags(parse_input(input), 'shiny gold') - 1

print('Number of bag colors containing at least one shiny gold bag (TEST):', get_number_of_colors(test_input_part1))
print('Number of bags contained in shiny gold bag (TEST):', get_number_of_contained_bags(test_input_part2))
with open('input.txt') as file:
    input = file.read()
    print('Number of bag colors containing at least one shiny gold bag:', get_number_of_colors(input))
    print('Number of bags contained in shiny gold bag:', get_number_of_contained_bags(input))