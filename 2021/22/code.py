test_input = '''on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682'''

def areoverlapping(cubeA, cubeB):
    xa, ya, za = cubeA
    xb, yb, zb = cubeB
    return (xb[0] >= xa[0] and xb[0] <= xa[1] or xa[0] >= xb[0] and xa[0] <= xb[1]) and \
        (yb[0] >= ya[0] and yb[0] <= ya[1] or ya[0] >= yb[0] and ya[0] <= yb[1]) and \
        (zb[0] >= za[0] and zb[0] <= za[1] or za[0] >= zb[0] and za[0] <= zb[1])

def get_instructions(input):
    cubes = []
    for line in input.strip().split('\n'):
        toggle, interval = line.split(' ')
        value = True if toggle == 'on' else False
        cubes.append({'value':value, 'range':[(int(a), int(b)) for (a,b) in [s.split('=')[1].split('..') for s in interval.split(',')]]})
    return cubes

def get_overlaps(cubes):
    overlapping = []
    for i,cube in enumerate(cubes):
        overlaps = []
        for j in range(i + 1, len(cubes)):
            other = cubes[j]
            if areoverlapping(cube['range'], other['range']):
                overlaps.append(other)
        overlapping.append(overlaps)
    return overlapping

def add(cubeA, cubeB):
    return [cubeA] + subtract(cubeB, cubeA)]

def part1(input):
    xa, xb = -50, 50
    ya, yb = -50, 50
    za, zb = -50, 50
    cubes = []
    for i in range(za, zb + 1):
        plane = []
        for j in range(ya, yb + 1):
            row = [0 for k in range(xa, xb + 1)]
            plane.append(row)
        cubes.append(plane)
    for ins in get_instructions(input):
        cube = ins['range'] 
        for z in range(max(za, cube[2][0]), min(zb, cube[2][1]) + 1):
            for y in range(max(ya, cube[1][0]), min(yb, cube[1][1]) + 1):
                for x in range(max(xa, cube[0][0]), min(xb, cube[0][1]) + 1):
                    cubes[z][y][x] = ins['value']
    total = sum([sum([sum(row) for row in plane]) for plane in cubes])
    print("Part 1: After executing the steps in the initialization region, there are {} cubes on".format(total))

def part2(input):
    instructions = get_instructions(input)
    cubes = []
    for ins in instructions:
        cube = ins['range']
        toggle_on = ins['value']
        if not cubes and toggle_on:
            cubes.append(cube)
        else:
            index = 0
            while index < len(cubes):
                other = cubes[index]
                if areoverlapping(other, cube):
                    if toggle_on:
                        pass
                    else:
                        pass

    print("Part 2:".format())

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)