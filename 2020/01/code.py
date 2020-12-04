from itertools import product

test_list = [
    1721,
    979,
    366,
    299,
    675,
    1456
]

def find_product_for_sum_of_values2(lst, n):
    return [(a * b, a, b) for (a, b) in product(lst, lst) if a + b == n]

def find_product_for_sum_of_values3(lst, n):
    return [(a * b * c, a, b, c) for ((a, b), c) in product(product(lst, lst), lst) if a + b + c == n]

print('Test1:', find_product_for_sum_of_values2(test_list, 2020)[0])
print('Test2:', find_product_for_sum_of_values3(test_list, 2020)[0])

#print(find_product_for_sum_of_values(test_list, 2020))
with open('input.txt') as file:
    lst = [int(x) for x in file.readlines()]
    print('Answer1:', find_product_for_sum_of_values2(lst, 2020)[0])
    print('Answer2:', find_product_for_sum_of_values3(lst, 2020)[0])