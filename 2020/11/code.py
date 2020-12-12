test_input = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''

def build_seat_layout(input):
    layout = [[c for c in row] for row in input.splitlines()]
    return layout

def get_seats_string(layout):
    return '\n'.join([''.join(row) for row in layout])

def update1(seats):
    updated_seats = [x[:] for x in seats]
    for i, row in enumerate(seats):
        for j, state in enumerate(row):
            if row[j] != '.':
                occupied = 0
                for k in (-1, 0, 1):
                    for l in (-1, 0, 1):
                        if k == 0 and l == 0:
                            continue
                        ik = i + k
                        jl = j + l
                        if ik >= 0 and ik < len(seats) and jl >= 0 and jl < len(row) and seats[ik][jl] == '#':
                            occupied +=1
                if state == 'L' and occupied == 0:
                    updated_seats[i][j] = '#'
                elif state == '#' and occupied >= 4:
                    updated_seats[i][j] = 'L'
    return updated_seats

def check_diagonal(seats, i, j, dx, dy):
    y, x = i + dy, j + dx
    while x >= 0 and x < len(seats[0]) and y >= 0 and y < len(seats):
        if seats[y][x] in ('#', 'L'):
            return seats[y][x] == '#'
        x += dx
        y += dy
    return False

def update2(seats):
    updated_seats = [x[:] for x in seats]
    for i, row in enumerate(seats):
        for j, state in enumerate(row):
            if i == 0 and j == 3:
                i = i
            if row[j] != '.':
                visible_seats = []
                for k in range(j + 1, len(row)):
                    if seats[i][k] in ('#', 'L'):
                        visible_seats.append(seats[i][k])
                        break
                for k in range(j, 0, -1):
                    if seats[i][k - 1]  in ('#', 'L'):
                        visible_seats.append(seats[i][k - 1])
                        break
                for k in range(i + 1, len(seats)):
                    if seats[k][j]  in ('#', 'L'):
                        visible_seats.append(seats[k][j])
                        break
                for k in range(i, 0, -1):
                    if seats[k - 1][j] in ('#', 'L'):
                        visible_seats.append(seats[k - 1][j])
                        break
                occupied = visible_seats.count('#')
                if check_diagonal(seats, i, j, 1, 1):
                    occupied +=1
                if check_diagonal(seats, i, j, 1, -1):
                    occupied +=1
                if check_diagonal(seats, i, j, -1, 1):
                    occupied +=1
                if check_diagonal(seats, i, j, -1, -1):
                    occupied +=1
                        
                if state == 'L' and occupied == 0:
                    updated_seats[i][j] = '#'
                elif state == '#' and occupied >= 5:
                    updated_seats[i][j] = 'L'
    return updated_seats

def find_occupation_count(input, update):
    layout = build_seat_layout(input)
    seats = layout
    seats_string = get_seats_string(layout)
    while True:
        next_seats = update(seats)
        next_seats_string = get_seats_string(next_seats)
        if next_seats_string == seats_string:
            break
        seats = next_seats
        seats_string = next_seats_string
    return seats_string.count('#')

print('Number of occupied seats part1 (TEST):', find_occupation_count(test_input, update1))
print('Number of occupied seats part2 (TEST):', find_occupation_count(test_input, update2))
with open('input.txt') as file:
    input = file.read()
    print('Number of occupied seats part1:', find_occupation_count(input, update1))
    print('Number of occupied seats part2:', find_occupation_count(input, update2))