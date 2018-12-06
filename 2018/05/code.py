from functools import reduce

def test(a, b):
    if not a:
        return b
    elif abs(ord(a[-1]) - ord(b[0])) == 32:
        return a[:-1]
    return a + b

def react(polymer):
    while True:
        oldpolymer = polymer
        polymer = reduce(test, list(polymer))
        if oldpolymer == polymer:
            return polymer

with open('input.txt') as f:
    #Part 1
    polymer = f.readline()[:-1]
    oldlen = len(polymer)
    polymer = react(polymer)

    newlen = len(polymer)
    print(oldlen, newlen)
    
with open('input.txt') as f:
    #Part 2
    original_polymer = f.readline()[:-1]
    orglen = len(original_polymer)
    lowest = orglen
    removed = None
    for unit in range(ord('A'), ord('Z') + 1):
        newpolymer = react(''.join(c for c in polymer if not (c == chr(unit) or c == chr(unit + 32))))
        print(chr(unit),chr(unit + 32), len(newpolymer))
        if len(newpolymer) < lowest:
            removed = unit
            lowest = len(newpolymer)

    newlen = lowest
    print(orglen, lowest, chr(removed))
