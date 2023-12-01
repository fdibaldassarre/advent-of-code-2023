#!/usr/bin/env python

DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        lines = list()
        with open(file) as hand:
            for line in hand:
                lines.append(line)
        self.data = lines

    def get_digit_simple(self, idx, line):
        ch = line[idx]
        if str.isdigit(ch):
            return ch
        else:
            return None

    def get_total(self, get_digit):
        tot = 0
        for line in self.data:
            number = ""
            for idx in range(len(line)):
                digit = get_digit(idx, line)
                if digit is not None:
                    number = digit
                    break
            for idx in range(len(line), 0, -1):
                digit = get_digit(idx - 1, line)
                if digit is not None:
                    number += digit
                    break
            tot += int(number)
        return tot

    def solve1(self):
        return self.get_total(self.get_digit_simple)

    def get_digit_or_name(self, idx, line):
        ch = line[idx]
        if str.isdigit(ch):
            return ch
        for candidate in DIGITS:
            end_idx = idx + len(candidate)
            if end_idx >= len(line):
                continue
            if line[idx:end_idx] == candidate:
                return DIGITS[candidate]
        return None

    def solve2(self):
        return self.get_total(self.get_digit_or_name)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
