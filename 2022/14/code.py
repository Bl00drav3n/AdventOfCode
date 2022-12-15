import time

test_input = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''

ROCK = '#'
AIR = ' '
SAND = 'o'
SOURCE = '+'

def in_bounds(field, p):
    return p[0] >= 0 and p[0] < len(field[0]) and p[1] >= 0 and p[1] < len(field)

def field_write(field, p, tile):
    field[p[1]][p[0]] = tile

def field_read(field, p):
    if in_bounds(field, p):
        return field[p[1]][p[0]]
    return AIR

def field_map(p, o):
    return (p[0] - o[0], p[1] - o[1])

def field_unmap(p, o):
    return (p[0] + o[0], p[1] + o[1])

def field_extend(field, o):
    width = len(field[0])
    o = (o[0] - width // 2, o[1])
    field = [[AIR for _ in range(width // 2)] + row + [AIR for _ in range(width // 2)] for row in field[:-1]]
    field.append([ROCK for _ in range(width + 2 * (width // 2))])
    return field, o

def cave(paths, source):
    minx = 1e9
    maxx = 0
    miny = 0
    maxy = 0
    for path in paths:
        for p in path:
            minx = min(minx, p[0])
            maxx = max(maxx, p[0])
            maxy = max(maxy, p[1])
    minx = min(minx, source[0])
    maxx = max(maxx, source[0]) + 1
    maxy += 1
    origin = (minx, miny)
    field = [[AIR for x in range(maxx - minx)] for y in range(maxy - miny)]
    field_write(field, field_map(source, origin), SOURCE)
    for path in paths:
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i+1]
            signx = 1 if p2[0] - p1[0] >= 0 else -1
            signy = 1 if p2[1] - p1[1] >= 0 else -1
            xstart = p1[0] if signx > 0 else p2[0]
            xend = p1[0] if signx < 0 else p2[0]
            ystart = p1[1] if signy > 0 else p2[1]
            yend = p1[1] if signy < 0 else p2[1]
            for y in range(ystart, yend + 1):
                for x in range(xstart, xend + 1):
                    field_write(field, field_map((x, y), origin), ROCK)
    return field, origin

def draw_cave(tiles, s=None):
    for j, row in enumerate(tiles):
        if s and s[1] == j:
            print(''.join(row[:s[0]]) + 'X' + ''.join(row[s[0]+1:]))
        else:
             print(''.join(row))
    print()

def simulate(input, ispart2):
    source_p = (500, 0)
    paths = [[tuple(map(int, p.split(','))) for p in row] for row in [line.split(' -> ') for line in input.strip().split('\n')]]
    field, o = cave(paths, source_p)

    if ispart2:
        field.append([AIR for _ in range(len(field[0]))])
        field.append([ROCK for _ in range(len(field[0]))])

    stop = False
    counter = 0
    while not stop and not field_read(field, field_map(source_p, o)) == SAND:
        sand = field_map(source_p, o)
        while True:
            p1 = (sand[0]    , sand[1] + 1)
            p2 = (sand[0] - 1, sand[1] + 1)
            p3 = (sand[0] + 1, sand[1] + 1)
            sand_next = None
            for p in [p1, p2, p3]:
                if p[0] == 20 and p[1] == 11:
                    p1 = p1
                if field_read(field, p) == AIR:
                    sand_next = p
                    break

            if sand_next:
                if in_bounds(field, p):
                    # We found a place to move to, continue
                    sand = tuple(sand_next)
                elif ispart2:
                    # We went outside the field
                    sand = field_unmap(sand, o)
                    sand_next = field_unmap(sand_next, o)
                    field, o = field_extend(field, o)
                    
                    # Fix glitching into rocks
                    if sand_next[1] != len(field) - 1 - o[1]:    
                        sand = field_map(sand_next, o)
                    else:
                        sand = field_map(sand, o)
                else:
                    stop = True
                    break
            else:
                # We found nowhere to go, so we rest here
                field_write(field, sand, SAND)
                counter += 1
                break
    return field, counter
    
def part1(input):
    if input:
        field, counter = simulate(input,False)
        print("Part 1: {}".format(counter))

def part2(input):
    field, counter = simulate(input,True)
    print("Part 2: {}".format(counter))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)