test_data = '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576'''

def validate(preamble, value):
    for i in range(0, len(preamble)):
        for j in range(i + 1, len(preamble)):
            if preamble[i] + preamble[j] == value:
                return True
    return False

def find_first_invalid_number(data, preamble_len):
    for i in range(preamble_len, len(data)):
        value = data[i]
        if not validate(data[i - preamble_len:i], value):
            return True, value
    return False, 0

def find_encryption_weakness(data, number):
    length = 2
    while True:
        for i in range(0, len(data)):
            sub_data = data[i:i+length]
            value = sum(sub_data)
            if value == number:
                return True, min(sub_data) + max(sub_data)
        length += 1
    return False, 0

def break_encoding(input, preamble_len):
    data = [int(x) for x in input.splitlines()]
    found, n = find_first_invalid_number(data, preamble_len)
    if found:
        print("First number that isn't the sum of any of the {} previous numbers: {}".format(preamble_len, n))
        found, m = find_encryption_weakness(data, n)
        if found:
            print("Encryption weakness is", m)
        else:
            print("No encryption weakness found")
    else:
        print("No invalid number found")

break_encoding(test_data, 5)
with open('input.txt') as file:
    break_encoding(file.read(), 25)