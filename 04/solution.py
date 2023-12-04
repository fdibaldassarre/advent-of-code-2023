#!/usr/bin/env python

class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                _, numbers_raw = line.split(": ")
                first_row, second_row = numbers_raw.split(" | ")
                first_numbers = list(map(int, first_row.split()))
                second_numbers = list(map(int, second_row.split()))
                self.data.append((first_numbers, second_numbers))

    def solve1(self):
        result = 0
        for winning_numbers, numbers_in_card in self.data:
            good = len(set(numbers_in_card) & set(winning_numbers))
            if good > 0:
                result += 2 ** (good - 1)
        return result

    def solve2(self):
        scratchcards = [1] * len(self.data)
        for i, scratchcard in enumerate(self.data):
            winning_numbers, numbers_in_card = scratchcard
            good = len(set(numbers_in_card) & set(winning_numbers))
            for j in range(i, i + good):
                scratchcards[j + 1] += scratchcards[i]
        return sum(scratchcards)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
