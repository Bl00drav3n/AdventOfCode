test_input = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''

from enum import IntEnum
from dataclasses import dataclass, field
from typing import ClassVar

class HandType(IntEnum):
    FIVE_OF_A_KIND  = 0
    FOUR_OF_A_KIND  = 1
    FULL_HOUSE      = 2
    THREE_OF_A_KIND = 3
    TWO_PAIR        = 4
    ONE_PAIR        = 5
    HIGH_CARD       = 6

    def type(hand):
        # Determine type of hand
        bins = {}
        for card in hand:
            if not card in bins:
                bins[card] = 0
            bins[card] += 1
        maxvalue = max(bins.values())
        if maxvalue == 5:
            return HandType.FIVE_OF_A_KIND
        elif maxvalue == 4:
            return HandType.FOUR_OF_A_KIND
        elif maxvalue == 3:
            return HandType.FULL_HOUSE if 2 in bins.values() else HandType.THREE_OF_A_KIND
        elif maxvalue == 2:
            return HandType.TWO_PAIR if list(bins.values()).count(2) == 2 else HandType.ONE_PAIR
        return HandType.HIGH_CARD

@dataclass
class Hand:
    hand: str
    bid: int
    type: HandType = field(init=False)
    
    order: ClassVar[str] = 'AKQJT98765432'
    
    def card_value(self, pos) -> int:
        # Value is determined by class variable order, the lower the better
        return self.order.find(self.hand[pos])
    
    def apply_jokers(self) -> None:
        # Bruteforce search for the best possible type
        if 'J' in self.hand:
            for card in self.order:
                hand = self.hand.replace('J', card)
                type = HandType.type(hand)
                if type < self.type:
                    self.type = type

    def __post_init__(self) -> None:
        self.type = HandType.type(self.hand)
    
    def __lt__(self, other) -> bool:
        # Comparison is done first by kind, then by card value
        assert len(self.hand) == len(other.hand)
        if self.type == other.type:
            for i in range(len(self.hand)):
                this_value = self.card_value(i)
                other_value = other.card_value(i)
                if this_value == other_value:
                    continue
                else:
                    return this_value < other_value
        return self.type < other.type

def generate_hands(input) -> list[Hand]:
    return [Hand(hand=pair[0], bid=int(pair[1])) for pair in [line.split(' ') for line in input.strip().split('\n')]]

def winnings(hands) -> int:
    return sum([(len(hands) - i) * hand.bid for i, hand in enumerate(sorted(hands))])

def part1(input):
    hands = generate_hands(input)
    result = winnings(hands)
    print("Part 1: The total winnings are {}".format(result))

def part2(input):
    Hand.order = "AKQT98765432J"
    hands = generate_hands(input)
    [hand.apply_jokers() for hand in hands]
    result = winnings(hands)
    print("Part 2: The total winnings are {}".format(result))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)