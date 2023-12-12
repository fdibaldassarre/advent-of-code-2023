#!/usr/bin/env python
import functools


class SpringGroup:

    def __init__(self, springs, groups):
        self.springs = springs
        self.groups = groups

    @functools.lru_cache(maxsize=None)
    def count_arrangements(self, pattern_idx=0, group_idx=0):
        group = self.groups[group_idx]

        possible_positions = 0
        n_springs = len(self.springs)
        for idx in range(pattern_idx, n_springs - group + 1):
            # group is [idx, idx + group)
            next_spring_idx = idx + group
            if "." not in self.springs[idx:next_spring_idx]:
                if group_idx == len(self.groups) - 1:
                    if next_spring_idx == n_springs or "#" not in self.springs[next_spring_idx:]:
                        possible_positions += 1
                elif next_spring_idx < n_springs and self.springs[next_spring_idx] in {".", "?"}:
                    possible_positions += self.count_arrangements(next_spring_idx + 1, group_idx + 1)
            if self.springs[idx] == "#":
                # group cannot start later than this
                break
        return possible_positions


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                springs, groups_str = line.split(" ")
                groups = tuple(map(int, groups_str.split(",")))
                self.data.append((springs, groups))

    def solve1(self):
        result = 0
        for spring_line in self.data:
            springs, groups = spring_line
            counter = SpringGroup(springs, groups)
            result += counter.count_arrangements()
        return result

    def solve2(self):
        result = 0
        for spring_line in self.data:
            springs, groups = spring_line
            springs = "?".join([springs] * 5)
            groups = groups * 5
            counter = SpringGroup(springs, groups)
            result += counter.count_arrangements()
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
