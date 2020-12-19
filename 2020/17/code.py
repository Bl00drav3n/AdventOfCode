test_input = '''.#.
..#
###
'''

ACTIVE = '#'
INACTIVE = '.'

def create_cubes(input):
    cubes = {}
    z = 0
    w = 0
    for y, row in enumerate(input):
        for x, cube in enumerate(row):
            cubes[(x, y, z, w)] = cube
    return cubes

def get_active_neighbors(cubes, coord):
    count = 0
    x, y, z, w = coord
    for l in [-1, 0, 1]:
        for k in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for i in [-1, 0, 1]:
                    if i == 0 and j == 0 and k == 0 and w == 0:
                        continue
                    test_coord = (x + i, y + j, z + k, w + l)
                    if test_coord in cubes and cubes[test_coord] == ACTIVE:
                        count += 1
    return count

def get_minmax(cubes):
    min_x = min_y = min_z = min_w = 10000000000000
    max_x = max_y = max_z = max_w = -10000000000000
    for (x, y, z, w) in cubes.keys():
        min_x = min(min_x, x - 1)
        min_y = min(min_y, y - 1)
        min_z = min(min_z, z - 1)
        min_w = min(min_w, w - 1)
        max_x = max(max_x, x + 1)
        max_y = max(max_y, y + 1)
        max_z = max(max_z, z + 1)
        max_w = max(max_w, w + 1)
    return (min_x, min_y, min_z, min_w), (max_x, max_y, max_z, max_w)

def update(cubes):
    tmp = {}
    (min_x, min_y, min_z, min_w), (max_x, max_y, max_z, max_w) = get_minmax(cubes)
    for w in range(min_w, max_w + 1):
        for z in range(min_z, max_z + 1):
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    coord = (x, y, z, w)
                    active_neighbors = get_active_neighbors(cubes, coord)
                    if coord in cubes:
                        if cubes[coord] == ACTIVE:
                            if active_neighbors in [2, 3]:
                                tmp[coord] = ACTIVE
                        elif active_neighbors == 3:
                            tmp[coord] = ACTIVE                        
                    elif active_neighbors == 3:
                        tmp[coord] = ACTIVE
    return tmp

def print_state(cubes):
    (min_x, min_y, min_z, min_w), (max_x, max_y, max_z, max_w) = get_minmax(cubes)
    for w in range(min_w, max_w + 1):
        for z in range(min_z, max_z + 1):
            print('\nz={}, w={}'.format(z, w))
            for y in range(min_y, max_y + 1):
                row = []
                for x in range(min_x, max_x + 1):
                    coord = (x, y, z, w)
                    cell = INACTIVE
                    if coord in cubes:
                        cell = cubes[coord]
                    row.append(cell)
                print(''.join(row))

def get_num_active_cubes(cubes):
    return len([value for value in cubes.values() if value == ACTIVE])

def run(input, cycles):
    cubes = create_cubes(input)
    print("\nBefore any cycles:")
    print_state(cubes)
    for i in range(0, cycles):
        cubes = update(cubes)
        print("\nAfter {} cycles:".format(i + 1))
        print_state(cubes)
    return get_num_active_cubes(cubes)

# TODO(rav3n): Algorithm broke when transitioning to 4D.
print("\nNumber of active cubes after 6 cycles (TEST):", run(test_input.splitlines(), 6))
with open('input.txt') as file:
    input = file.readlines()
    print("\nNumber of active cubes after 6 cycles:", run(input, 6))