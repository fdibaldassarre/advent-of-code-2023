#!/usr/bin/env python
import math


class Solver:

    def __init__(self):
        self.times = None
        self.distances = None

    def parse(self, file):
        with open(file) as hand:
            time_raw = hand.readline()[len("Time:"):].strip()
            distance_raw = hand.readline()[len("Distance:"):].strip()
            self.times = list(map(int, time_raw.split()))
            self.distances = list(map(int, distance_raw.split()))

    def _beat_record(self, duration, record):
        delta = (duration ** 2 - 4 * record) ** 0.5
        x_1 = (duration - delta) / 2
        x_2 = (duration + delta) / 2
        if x_1.is_integer():
            x_1 = int(x_1) + 1
        else:
            x_1 = int(math.ceil(x_1))
        if x_2.is_integer():
            x_2 = int(x_2) - 1
        else:
            x_2 = int(math.floor(x_2))
        return x_1, x_2

    def solve1(self):
        possible_wins = 1
        for duration, record in zip(self.times, self.distances):
            valid_min, valid_max = self._beat_record(duration, record)
            possible_wins *= (valid_max - valid_min + 1)
        return possible_wins

    def solve2(self):
        single_duration = int("".join(map(str, self.times)))
        single_record = int("".join(map(str, self.distances)))
        valid_min, valid_max = self._beat_record(single_duration, single_record)
        return valid_max - valid_min + 1


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
