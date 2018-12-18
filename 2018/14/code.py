puzzle_input = 430971

#PART 1
A = 0
B = 1
recipes = [3, 7]
while len(recipes) < puzzle_input + 10:
    s = recipes[A] + recipes[B]
    if s < 10:
        recipes.append(s)
    else:
        recipes.append(s // 10)
        recipes.append(s % 10)
    A = (A + recipes[A] + 1) % len(recipes)
    B = (B + recipes[B] + 1) % len(recipes)

print(recipes[puzzle_input:puzzle_input + 10])

#PART 2
def to_digits(n):
    digits = []
    while n:
        digits.append(n % 10)
        n //= 10
    digits.reverse()
    return digits

A = 8
B = 4
recipes = [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9, 2]
pattern = to_digits(puzzle_input)
while True:
    s = recipes[A] + recipes[B]
    if s < 10:
        recipes.append(s)
        test = recipes[-len(pattern):]
        if test == pattern:
            print(len(recipes) - len(pattern))
            break
    else:
        recipes.append(s // 10)
        test = recipes[-len(pattern):]
        if test == pattern:
            print(len(recipes) - len(pattern))
            break

        recipes.append(s % 10)
        test = recipes[-len(pattern):]
        if test == pattern:
            print(len(recipes) - len(pattern))
            break

    A = (A + recipes[A] + 1) % len(recipes)
    B = (B + recipes[B] + 1) % len(recipes)
    