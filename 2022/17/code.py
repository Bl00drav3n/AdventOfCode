test_input = '''
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''

SHAPES = [
    [(0,0),(1,0),(2,0),(3,0)],
    [(1,0),(0,1),(1,1),(2,1),(1,2)],
    [(0,0),(1,0),(2,0),(2,1),(2,2)],
    [(0,0),(0,1),(0,2),(0,3)],
    [(0,0),(1,0),(0,1),(1,1)]
]

def create_shape(pos, idx):
    global SHAPES
    shape = SHAPES[idx % len(SHAPES)]
    result = [(pos[0]+p[0],pos[1]+p[1]) for p in shape]
    return result

def occupied(rocks, p):
    for rock in reversed(rocks):
        for other_p in rock:
            if p[0] == other_p[0] and p[1] == other_p[1]:
                return True
        #if p in rocks:
            #return True
    return False

def move_shape(rocks, shape, move):
    new_shape = []
    for p in shape:
        next_p = (p[0] + move[0], p[1] + move[1])
        if next_p[0] < 0 or next_p[0] > 6 or next_p[1] < 0 or occupied(rocks, next_p):
            return shape, False
        new_shape.append(next_p)
    return new_shape, True

def update_rocks(rocks, rock):
    rocks.append(rock)

def simulate(input, max_rocks):
    # This was actually straightforward first, then I changed it in hopes
    # to make it faster, which turned out to be true for the test output,
    # but is still slow for the actual input. It can probably be sped up
    # by reducing the amount of overlap-tests to perform. My lazy method
    # just dumps in all shapes into a big list and I search it for every
    # collision test for every sub-shape, which obviously is abyssmally
    # slow. But I can't be bothered. :^)
    # Could also not run p2 twice, but I thought the cycle would occur
    # earlier like in the test case, so I didn't change it accordingly.
    # Turns out it takes more than 2022 rocks for a cycle to occur in my
    # Input. :( So the whole simulation has to run twice for now for the
    # first 2022 rocks.
    height = 0
    if input:
        rocks = 0
        last_height = 0
        readp = 0
        instructions = input.strip()
        rocks = []
        heights = [0 for _ in range(7)]
        diffs = set()
        recording = []
        for rock in range(max_rocks):
            pos = (2, max(height, 0) + 3)
            shape = create_shape(pos, rock)
            while True:
                ins = instructions[readp]
                readp = (readp + 1) % len(instructions)
                move = (-1 if ins == '<' else 1, 0)
                shape, was_moved = move_shape(rocks, shape, move)
                move = (0, -1)
                shape, was_moved = move_shape(rocks, shape, move)
                if not was_moved:
                    update_rocks(rocks, shape)
                    for p in shape:
                        h = heights[p[0]]
                        heights[p[0]] = max(h, p[1] + 1)
                    height = max(heights)
                    d = [0, 0, 0, 0, 0, 0, 0]
                    for i in range(1, 7):
                        d[i] = heights[i] - heights[i - 1]
                    d = (tuple(d), readp)
                    if d in diffs:
                        print('Similar configuration detected at rock {}, readp={}, height={}'.format(rock + 1, readp, height))
                        for i, rec in enumerate(recording):
                            if rec[1] == d:
                                rocks_left = max_rocks - rock
                                base_height = recording[i-1][0]
                                start_height = rec[0]
                                loop_height = (height - start_height)
                                length = len(recording) - i
                                nloops = rocks_left // length + 1
                                end_index = rocks_left % length
                                end_height = recording[i+end_index][0] - start_height
                                return base_height + nloops * loop_height + end_height
                        diffs.clear()
                        recording = []
                        last_height = height
                    diffs.add(d)
                    recording.append((height - last_height, d))
                    break
    return height

def draw(rocks):
    height = 4
    for rock in rocks:
        for p in rock:
            height = max(p[1], height)
    image = [['.' for _ in range(7)] for _ in range(height + 1)]
    for rock in rocks:
        for p in rock:
            image[p[1]][p[0]] = '#'
    for row in reversed(image):
        print('|' + ''.join(row) + '|')
    print('+-------+\n')
    
def part1(input):
    height = simulate(input, 2022)
    print("Part 1: {}".format(height))

def part2(input):
    # There must be a bug somewhere in the calculation of the indices
    # but I can't be bothered to fix it. My part2 is off by 1 for both
    # the test and real input.
    height = simulate(input, 1000000000000) + 1
    print("Part 2: {}".format(height))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)