test_input = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''

def transpose(input):
    tmp = bytearray()
    lines = input.split("\n")
    for i in range(len(lines[0])):
        for line in lines:
            tmp.append(ord(line[i]))
        tmp.append(ord('\n'))
    return bytes(tmp).decode()

def check_diag1(string, lines, x, y):
    check = True
    if(x < len(lines) - 3 and y < len(lines) - 3):
        for i in range(4):
            check = check and lines[y+i][x+i] == string[i]
    else:
        check = False
    return check

def check_diag2(string, lines, x, y):
    # Can just reverse the lines and reuse first check
    return check_diag1(string, lines[::-1], x, y)

def check3x3(lines, x, y):
    test = "".join([lines[y - 1][x - 1], lines[y - 1][x + 1], lines[y + 1][x - 1], lines[y + 1][x + 1]])
    return test == "MMSS" or test == "SSMM" or test == "MSMS" or test == "SMSM"

def xmas_kernel(lines, x, y, width, height):
    result = 0
    if x > 0 and x < width - 1 and y > 0 and y < height - 1:
        if lines[y][x] == 'A':
            if(check3x3(lines, x, y)):
                result = 1
    return result

def part1(input):
    XMAS = "XMAS"
    SAMX = "SAMX"
    
    string = input.strip()
    transposed_string = transpose(string)

    XMAS = "XMAS"
    count = 0
    count += string.count(XMAS) # Forwards direction
    count += string[::-1].count(XMAS) # Backwards direction
    count += transposed_string.count(XMAS) # Vertical forwards direction
    count += transposed_string[::-1].count(XMAS) # Vertical backwards direction

    # Pesky diagonals
    lines = string.split('\n')
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if check_diag1(XMAS, lines, x, y):
                count += 1
            if check_diag1(SAMX, lines, x, y):
                count += 1
            if check_diag2(XMAS, lines, x, y):
                count += 1
            if check_diag2(SAMX, lines, x, y):
                count += 1

    print("Part 1: Count: {}".format(count))

def part2(input):
    lines = input.strip().split('\n')
    width = len(lines[0])
    height = len(lines)
    count = 0
    for y in range(height):
        for x in range(width):
            count += xmas_kernel(lines, x, y, width, height)

    print("Part 2: {}".format(count))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)