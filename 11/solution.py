#!/usr/bin/env python

class Solver:

    def __init__(self):
        self.data = None
        self.max_x = -1
        self.max_y = -1

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for y, line in enumerate(hand):
                self.max_y = max(self.max_y, y)
                line = line.strip()
                for x, el in enumerate(line):
                    self.max_x = max(self.max_x, x)
                    if el == "#":
                        self.data.append((x, y))

    def get_distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return dx + dy

    def _get_double_rows(self):
        dx = [0] * (self.max_x + 1)
        current_dx = 0
        for x in range(self.max_x + 1):
            is_empty = True
            for y in range(self.max_y + 1):
                if (x, y) in self.data:
                    is_empty = False
                    break
            if is_empty:
                current_dx += 1
            dx[x] = current_dx
        return dx

    def _get_double_columns(self):
        dy = [0] * (self.max_y + 1)
        current_dy = 0
        for y in range(self.max_y + 1):
            is_empty = True
            for x in range(self.max_x + 1):
                if (x, y) in self.data:
                    is_empty = False
                    break
            if is_empty:
                current_dy += 1
            dy[y] = current_dy
        return dy

    def solve(self, rate):
        dx = self._get_double_rows()
        dy = self._get_double_columns()

        def _convert(p):
            x, y = p
            return x + dx[x] * (rate - 1), y + dy[y] * (rate - 1)

        sum_shortest = 0
        for i, p1 in enumerate(self.data):
            for j in range(i + 1, len(self.data)):
                p2 = self.data[j]
                c1 = _convert(p1)
                c2 = _convert(p2)
                sum_shortest += self.get_distance(c1, c2)
        return sum_shortest

    def solve1(self):
        return self.solve(rate=2)

    def solve2(self):
        return self.solve(rate=1000000)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
