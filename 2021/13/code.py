test_input = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''

def read_input(input):
    first, second = input.strip().split('\n\n')
    marks = set([(int(x), int(y)) for (x, y) in [p.split(',') for p in first.split('\n')]])
    return marks, second.split('\n')

def mirror(p, s):
    return 2 * s - p

def fold(marks, ins):
    ins = ins.split(' ')[2]
    axis, value = ins.split('=')
    value = int(value)
    folded = set()
    while marks:
        mark = marks.pop()
        if axis == 'x':
            if mark[0] > value:
                mark = (mirror(mark[0], value), mark[1])
        else:
            if mark[1] > value:
                mark = (mark[0], mirror(mark[1], value))
        folded.add(mark)
    return folded

def print_marks(marks):
    field = []
    for i in range(max([y for x, y in marks]) + 1):
        field.append(['.'] * (max(x for x, y in marks) + 1))
    for x, y in marks:
        field[y][x] = '#'
    [print(''.join(row)) for row in field]
    print()

def part1(input):
    marks, ins = read_input(input)
    marks = fold(marks, ins[0])
    print("Part 1: There are {} dots visible after the first fold instruction".format(len(marks)))

def part2(input):
    marks, instructions = read_input(input)
    for ins in instructions:
        marks = fold(marks, ins)
    print("Part 2: The code to activate the infrared thermal imaging camera system is".format())
    print_marks(marks)

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)