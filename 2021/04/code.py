import io

test_input = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7'''

def process_input(input):
    # Read values
    buffer = io.StringIO(input)
    numbers = [int(val) for val in buffer.readline().strip().split(',')]

    buffer.readline()

    # Read boards
    boards = buffer.read().split('\n\n')
    for i, board in enumerate(boards):
        boards[i] = [[int(val) for val in row.split()] for row in board.strip().split('\n')]
    return numbers, boards

def update_and_check_winning(board, n):
    # Mark winning numbers as -1
    for r, row in enumerate(board):
        board[r] = [m if m != n else -1 for m in board[r]]
    # Check rows and columns (a sum of -5 means winning)
    for row in board:
        if sum(row) == -5:
            return True
    for col in range(0, 5):
        if sum([row[col] for row in board]) == -5:
            return True
    return False

def order_winning_boards(input):
    numbers, boards = process_input(input)
    ordered_boards = []
    for n in numbers:
        # Find list of winning boards of this round
        winning_boards = []
        for board in boards:
            if update_and_check_winning(board, n):
                winning_boards.append(board)
        # Remove winning boards from the original list and move them into the ordered list
        if winning_boards:
            for winning_board in winning_boards:
                ordered_boards.append((winning_board, n))
                boards.remove(winning_board)
    return ordered_boards

def get_score(board, winning_number):
    return sum([sum([n for n in row if n != -1]) for row in board]) * winning_number

def part1(input):
    board, last = order_winning_boards(input)[0]
    print("Part 1: The final score of the first winning board is {}".format(get_score(board, last)))

def part2(input):
    board, last = order_winning_boards(input)[-1]
    print("Part 2: The final score of the last winning board is {}".format(get_score(board, last)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    print('---INPUT---')
    input = f.read()
    part1(input)
    part2(input)