test_inputs = '''FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
'''

def get_seat_id(string):
    return int(string.replace('R', 'B').replace('L', 'F').replace('F', '0').replace('B', '1'), 2)

def seat_info_from_id(seat_id):
    row = seat_id >> 3
    col = seat_id & 7
    return seat_id, row, col

def get_seat_info(seat_string):
    seat_id = get_seat_id(seat_string)
    return seat_info_from_id(seat_id)

def find_seat_id(seat_infos):
    infos = iter(seat_infos)
    info = next(infos)
    for next_info in infos:
        diff = info[0] - next_info[0]
        if diff > 1:
            return seat_info_from_id(info[0] - 1)
        info = next_info

for input in test_inputs.splitlines():
    string = input.strip()
    print('TEST:', string, get_seat_info(string))

with open('input.txt') as file:
    seat_infos = []
    for line in file.readlines():
        seat_info = get_seat_info(line)
        seat_infos.append(seat_info)
    seat_infos.sort(key=lambda info:info[0], reverse=True)
    info = seat_infos[0]
    print('Highest seat id:', info)
    print('My seat id is:', find_seat_id(seat_infos))