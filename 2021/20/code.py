import time

test_input = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###'''

def get_outside_pixel(algo, it):
    if algo[0] == '#' and algo[511] == '.':
        return 0 if it % 2 == 0 else 1
    return 0

def get_pixel(img, algo, it, x, y):
    if y < 0 or y >= len(img) or x < 0 or x >= len(img[y]):
        return get_outside_pixel(algo, it)
    return img[y][x]

def lookup(algo, n):
    return 1 if algo[n] == '#' else 0

def apply(img, algo, it):
    img_next = [[0 for i in range(len(img[0]) + 6)] for j in range(len(img) + 6)]
    for y in range(0, len(img_next)):
        for x in range(0, len(img_next[y])):
            n = 0
            for iy in [y - 1, y, y + 1]:
                for ix in [x - 1, x , x + 1]:
                    n <<= 1
                    n += get_pixel(img, algo, it, ix - 2, iy - 2)
            img_next[y][x] = lookup(algo, n)
    return img_next

def print_image(img):
    print('\n'.join([''.join(['.' if v == 0 else '#' for v in row]) for row in img]))
    print()

def enhance(input, n):
    algo, img = input.strip().split('\n\n')
    img = [[1 if c== '#' else 0 for c in row ] for row in img.split('\n')]
    #print_image(img)
    t0 = time.time_ns()
    for i in range(n):
        #print(i)
        img = apply(img, algo, i)
        #print_image(img)
    result = sum([sum(row) for row in img])
    t1 = time.time_ns()
    return result, (t1 - t0) / 1e9

def part1(input):
    n = 2
    answer, t = enhance(input, n)
    print("Part 1: After {} steps, there are {} pixels lit ({}s)".format(n, answer, t))

def part2(input):
    n = 50
    answer, t = enhance(input, n)
    print("Part 2: After {} steps, there are {} pixels lit ({}s)".format(n, answer, t))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)