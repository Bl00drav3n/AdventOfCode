test_input1 = '''16
10
15
5
1
11
7
19
6
12
4'''.splitlines()

test_input2 = '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3'''.splitlines()

def get_joltage_differences(input):
    adapters = [int(x) for x in input]
    adapters.sort()
    return list(map(lambda x, y: x - y, adapters + [adapters[-1] + 3], [0] + adapters))

def get_joltage_mul(input):
    joltage_differences = get_joltage_differences(input)
    one_jolts = joltage_differences.count(1)
    three_jolts = joltage_differences.count(3)
    return one_jolts * three_jolts

def get_number_of_arrangements(input):
    diffstr = ','.join([str(x) for x in get_joltage_differences(input)])
    run11113 = diffstr.count('1,1,1,1,3')
    diffstr = diffstr.replace('1,1,1,1,3', '')
    run1113 = diffstr.count('1,1,1,3')
    diffstr = diffstr.replace('1,1,1,3', '')
    run113 = diffstr.count('1,1,3')
    return pow(2, run113) * pow(4, run1113) * pow(7, run11113)

print('Product of # of 1 and # of 3 (TEST1):', get_joltage_mul(test_input1))
print('Number of arrangements (TEST1):', get_number_of_arrangements(test_input1))
print('Product of # of 1 and # of 3 (TEST2):', get_joltage_mul(test_input2))
print('Number of arrangements (TEST2):', get_number_of_arrangements(test_input2))
with open('input.txt') as file:
    input = file.read().splitlines()
    print('Product of # of 1 and # of 3:', get_joltage_mul(input))
    print('Number of arrangements:', get_number_of_arrangements(input))