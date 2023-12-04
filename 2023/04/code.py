test_input = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''

def read_cards(input):
    return [(list(map(int, pair[0].split(' '))), list(map(int, pair[1].split(' ')))) for pair in [[s.strip() for s in line.split(':')[1].split('|')] for line in input.strip().replace('  ', ' ').split('\n')]]

def winning_count(cards):
    return [len([winning for winning in card[1] if winning in card[0]]) for card in cards]

def part1(input):
    cards = read_cards(input)
    points = sum(map(lambda n: 2**(n - 1) if n > 0 else 0, winning_count(cards)))
    print("Part 1: The cards are worth a total of {} points".format(points))

def part2(input):
    cards = read_cards(input)
    card_counts = [1] * len(cards)
    winning = winning_count(cards)
    for i in range(len(card_counts)):
        copies = winning[i]
        for j in range(min(copies, len(card_counts) - i - 1)):
            card_counts[i+j+1] += card_counts[i]
    print("Part 2: We end up with {} scartchards".format(sum(card_counts)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)