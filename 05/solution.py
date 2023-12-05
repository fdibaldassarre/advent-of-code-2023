#!/usr/bin/env python
import bisect
import collections


class Solver:

    def __init__(self):
        self.seeds = None
        self.maps = dict()

    def parse(self, file):
        with open(file) as hand:
            seeds_line = next(hand)
            seeds_line = seeds_line.strip().split(": ")[1]
            self.seeds = list(map(int, seeds_line.split(" ")))
            current_map = None
            for line in hand:
                line = line.strip()
                if line == "":
                    if current_map is not None:
                        source, target, values = current_map
                        self.maps[source] = (target, values)
                    current_map = None
                elif current_map is None:
                    source, target = line.split(" ")[0].split("-to-")
                    current_values = list()
                    current_map = (source, target, current_values)
                else:
                    current_values = current_map[2]
                    dest_start, source_start, value_range = tuple(
                        map(int, line.split(" "))
                    )
                    current_values.append((dest_start, source_start, value_range))
            if current_map is not None:
                source, target, values = current_map
                self.maps[source] = (target, values)
            for _, values in self.maps.values():
                values.sort(key=lambda el: el[1])

    def solve1(self):
        lowest_result = None
        for seed in self.seeds:
            source_value = seed
            source = "seed"
            while source != "location":
                target, values = self.maps[source]
                destination_value = None
                for d_start, s_start, v_range in values:
                    delta = source_value - s_start
                    if 0 <= delta < v_range:
                        destination_value = d_start + delta
                        break
                if destination_value is not None:
                    source_value = destination_value
                source = target
            if lowest_result is None:
                lowest_result = source_value
            else:
                lowest_result = min(lowest_result, source_value)
        return lowest_result

    def solve2(self):
        ranges = collections.deque()
        for i in range(len(self.seeds) // 2):
            start, r_range = self.seeds[2 * i], self.seeds[2 * i + 1]
            ranges.append((start, r_range))
        source = "seed"
        while source != "location":
            target, values = self.maps[source]
            new_ranges = collections.deque()
            while len(ranges) > 0:
                current_start, current_range = ranges.pop()
                idx = bisect.bisect_right(values, current_start, key=lambda el: el[1]) - 1
                if idx < 0:
                    new_ranges.append((current_start, current_range))
                    continue
                # s_start <= current_start < current_end
                d_start, s_start, v_range = values[idx]
                s_end = s_start + v_range
                current_end = current_start + current_range
                if s_end <= current_start:
                    new_ranges.append((current_start, current_range))
                    continue
                # s_start <= current_start < s_end
                start_delta = current_start - s_start
                if current_end <= s_end:
                    new_ranges.append((d_start + start_delta, current_range))
                else:
                    # s_start <= current_start < s_end < current_end
                    max_range = s_end - current_start
                    new_ranges.append((d_start + start_delta, max_range))
                    ranges.append((current_start + max_range, current_range - max_range))
            source = target
            ranges = new_ranges
        return min(map(lambda el: el[0], ranges))


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
