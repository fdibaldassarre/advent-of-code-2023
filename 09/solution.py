#!/usr/bin/env python
import functools
from typing import List


class HistorySolver:

    def __init__(self, line: List[int]):
        self.line = line
        self.cache = dict()

    def _get_next(self, x: int, y: int) -> int:
        if (x, y) not in self.cache:
            value = self._compute_next(x, y)
            self.cache[(x, y)] = value
        return self.cache[(x, y)]

    def _compute_next(self, x: int, y: int) -> int:
        if x < len(self.line) - y:
            if y == 0:
                return self.line[x]
            else:
                return self._get_next(x + 1, y - 1) - self._get_next(x, y - 1)

        # End condition
        v = self._get_next(x - 1, y)
        if v == self._get_next(x - 2, y):
            return v

        # Iterate
        return self._get_next(x - 1, y) + self._get_next(x - 1, y + 1)

    def solve(self):
        return self._get_next(len(self.line), 0)


class HistorySolver2:

    def __init__(self, line: List[int]):
        self.line = line
        self.cache = dict()

    def _get_next(self, x: int, y: int) -> int:
        if (x, y) not in self.cache:
            value = self._compute_next(x, y)
            self.cache[(x, y)] = value
        return self.cache[(x, y)]

    def _compute_next(self, x: int, y: int) -> int:
        if x >= 0:
            if y == 0:
                return self.line[x]
            else:
                return self._get_next(x + 1, y - 1) - self._get_next(x, y - 1)

        # End condition
        v = self._get_next(0, y)
        if v == self._get_next(1, y) and v == 0:
            return v

        # Iterate
        return self._get_next(0, y) - self._get_next(-1, y + 1)

    def solve(self):
        return self._get_next(-1, 0)


class Solver:

    def __init__(self):
        self.data = None
        self.cache = dict()

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                values = line.strip().split(" ")
                self.data.append(list(map(int, values)))

    def solve1(self):
        result = 0
        for values in self.data:
            solver = HistorySolver(values)
            res = solver.solve()
            result += res
        return result

    def solve2(self):
        result = 0
        for values in self.data:
            solver = HistorySolver2(values)
            res = solver.solve()
            result += res
        return result


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
