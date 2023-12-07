#!/usr/bin/env python

from collections import Counter
from typing import List

CARDS = "AKQJT98765432"
CARDS_TO_VALUE = {card: -idx for idx, card in enumerate(CARDS)}

CARDS_ALT = "AKQT98765432J"
CARDS_ALT_TO_VALUE = {card: -idx for idx, card in enumerate(CARDS_ALT)}


def get_hand_type(cards: str) -> int:
    c = Counter(cards)
    n_distincts = len(c.items())
    if n_distincts == 5:
        # High card
        return 1
    if n_distincts == 4:
        # One pair
        return 2
    if n_distincts == 3:
        if c.most_common(n=1)[0][1] == 2:
            # Two pairs
            return 3
        else:
            # Tris
            return 4
    if n_distincts == 2:
        if c.most_common(n=1)[0][1] == 3:
            # Full house
            return 5
        else:
            # Four-of-a-kind
            return 6
    # Five of a kind
    return 7


def get_hand_type_joking(cards: str) -> int:
    if "J" not in cards:
        return get_hand_type(cards)
    # I have at least one joker
    others = ""
    n_jokers = 0
    for card in cards:
        if card == "J":
            n_jokers += 1
        else:
            others += card
    c = Counter(others)
    n_distinct = len(c.items())
    if n_distinct == 1:
        # Five of a kind
        return 7
    if n_jokers >= 4:
        # 1 or 0 Cards
        # Five of a kind
        return 7
    if n_jokers == 3:
        # 2 Cards
        # n_distinct == 2
        # Four-of-a-kind
        return 6
    if n_jokers == 2:
        # 3 Cards
        if n_distinct == 2:
            # 2 + 1
            # Four-of-a-kind
            return 6
        else:
            # 1 + 1 + 1
            # n_distinct = 3
            # Tris
            return 4
    # n_jokers == 1
    # 4 Cards
    if n_distinct == 2:
        if c.most_common(n=1)[0][1] == 3:
            # 3 + 1
            # Four-of-a-kind
            return 6
        else:
            # 2 + 2
            # Full house
            return 5
    if n_distinct == 3:
        # 2 + 1 + 1
        # Tris
        return 4
    # n_distinct == 4:
    # One pair
    return 2


class CardHand:

    def __init__(self, cards: List[int], hand_type: int):
        self.cards = cards
        self.hand_type = hand_type

    def __lt__(self, other):
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        for i in range(5):
            if self.cards[i] != other.cards[i]:
                return self.cards[i] < other.cards[i]

    @classmethod
    def build(cls, cards: str):
        cards_values = list(map(CARDS_TO_VALUE.get, cards))
        hand_type = get_hand_type(cards)
        return CardHand(cards_values, hand_type)

    @classmethod
    def build_alternative(cls, cards: str):
        cards_values = list(map(CARDS_ALT_TO_VALUE.get, cards))
        hand_type = get_hand_type_joking(cards)
        return CardHand(cards_values, hand_type)


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip().split(" ")
                cards, bid = line
                bid = int(bid)
                self.data.append((cards, bid))

    def _solve(self, build_func):
        hands = list()
        for row in self.data:
            cards, bid = row
            hands.append((build_func(cards), bid))

        hands.sort()

        score = 0
        for i, hand in enumerate(hands):
            _, bid = hand
            score += (i + 1) * bid

        return score

    def solve1(self):
        return self._solve(CardHand.build)

    def solve2(self):
        return self._solve(CardHand.build_alternative)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
