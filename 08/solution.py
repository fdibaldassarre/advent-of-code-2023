#!/usr/bin/env python
import math


class Solver:

    def __init__(self):
        self.steps = None
        self.data = None

    def parse(self, file):
        self.data = dict()
        with open(file) as hand:
            self.steps = hand.readline().strip()
            hand.readline()
            for line in hand:
                line = line.strip().split(" = ")
                source, targets_raw = line
                left, right = targets_raw[1:-1].split(", ")
                self.data[source] = (left, right)

    def _go_to_next(self, step_idx, current_location):
        left, right = self.data[current_location]
        if self.steps[step_idx] == "L":
            return left
        else:
            return right

    def solve1(self):
        current_location = "AAA"
        steps_done = 0
        while current_location != "ZZZ":
            steps_idx = steps_done % len(self.steps)
            current_location = self._go_to_next(steps_idx, current_location)
            steps_done += 1
        return steps_done

    def _get_location_periods(self, location):
        steps_done = 0
        period = 0
        while not location.endswith("Z"):
            steps_idx = steps_done % len(self.steps)
            location = self._go_to_next(steps_idx, location)
            steps_done += 1
            if location.endswith("Z"):
                period = steps_done
                break
        return period

    def solve2(self):
        periods = list()
        for node in self.data.keys():
            if node.endswith("A"):
                periods.append(self._get_location_periods(node))
        return math.lcm(*periods)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
