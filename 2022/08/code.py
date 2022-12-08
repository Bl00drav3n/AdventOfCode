test_input = '''30373
25512
65332
33549
35390
'''

# Slice of row
def row(trees, i):
    return trees[i]

# Slice of column
def column(trees, i):
    return [line[i] for line in trees]

# Piece of cake
def visible(trees, row_id, col_id):
    # Just so we don't crash if there is no input
    if row_id >= len(trees) or col_id >= len(trees[0]) or col_id <= 0 or row_id <= 0:
        return False

    h = trees[row_id][col_id]
    r = row(trees, row_id)
    c = column(trees, col_id)
    return max(r[:col_id]) < h or max(r[col_id+1:]) < h or max(c[:row_id]) < h or max(c[row_id+1:]) < h

# Dont be lazy
def view_distance(h, trees):
    for i in range(len((trees))):
        if h <= trees[i]:
            return i + 1
    return len(trees)

# You gotta do the cooking by the book
def scenic_score(trees, row_id, col_id):
    if row_id >= len(trees) or col_id >= len(trees[0]) or col_id <= 0 or row_id <= 0:
        return 0

    h = trees[row_id][col_id]
    r = row(trees, row_id)
    c = column(trees, col_id)
    left  = view_distance(h, list(reversed(r[:col_id])))
    right = view_distance(h, r[col_id+1:])
    up    = view_distance(h, list(reversed(c[:row_id])))
    down  = view_distance(h, c[row_id+1:])
    return left * right * up * down

def parse_input(input):
    trees = [list(map(int, line)) for line in input.strip().split('\n')]
    nrow = len(trees)
    ncol = len(trees[0])
    return trees, nrow, ncol

def part1(input):
    trees, nrow, ncol = parse_input(input)
    visible_interior_trees = list(filter(lambda id: visible(trees, id[0], id[1]), [(idx % (ncol - 2) + 1, idx // (ncol - 2) + 1) for idx in range((nrow - 2) * (ncol - 2))]))
    total = 2 * (nrow + ncol - 2) + len(visible_interior_trees)
    print("Part 1: {}".format(total))

def part2(input):
    trees, nrow, ncol = parse_input(input)
    best_score = max([max([scenic_score(trees, j, i) for i in range(len(row))]) for j, row in enumerate(trees)])
    print("Part 2: {}".format(best_score))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)