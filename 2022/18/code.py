test_input = '''
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

def get_cubes(input):
    if input:
        cube_coords = [tuple(map(int, row.split(','))) for row in input.strip().split('\n')]
        cubes = [[] for _ in range(len(cube_coords))]
        for i in range(0, len(cube_coords)):
            cube_i = cube_coords[i]
            for j in range(i, len(cube_coords)):
                cube_j = cube_coords[j]
                if distance(cube_i, cube_j) == 1:
                    cubes[i].append(j)
                    cubes[j].append(i)
        return cubes

def part1(input):
    cubes = get_cubes(input)
    result = sum(map(lambda lst: 6 - len(lst), cubes))
    print("Part 1: {}".format(result))

def part2(input):
    print("Part 2:".format())

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)