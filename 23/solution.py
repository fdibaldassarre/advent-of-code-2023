#!/usr/bin/env python
import collections
from typing import Tuple, Set


def get_direction(start, end):
    sx, sy = start
    ex, ey = end
    return ex - sx, ey - sy


ARROW_TO_DIRECTION = {
    ">": (1, 0),
    "<": (-1, 0),
    "v": (0, 1),
    "^": (0, -1),
}

class Path:

    def __init__(self, start, end, length, conjunctions=None):
        self.start = start
        self.end = end
        self.length = length
        self.conjunctions = set() if conjunctions is None else conjunctions

    def __str__(self):
        return f"{str(self.start)} -> {str(self.end)}: steps {self.length}\n conjunctions: {str(self.conjunctions)}"


class Solver:

    def __init__(self):
        self.data = None
        self.source = None
        self.target = None
        self.width = 0
        self.height = 0
        self.ignore_slopes = False

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                self.data.append(line)
        for x, el in enumerate(self.data[0]):
            if el == ".":
                self.source = (x, 0)
        for x, el in enumerate(self.data[-1]):
            if el == ".":
                self.target = (x, len(self.data) - 1)
        self.width = len(self.data[0])
        self.height = len(self.data)

    def _get_neighbours(self, point: Tuple[int, int], prev: Tuple[int, int] | None) -> Set[Tuple[int, int]]:
        x, y = point
        neighbours = set()
        for candidate in [(x-1, y), (x+1, y), (x, y+1), (x, y-1)]:
            if candidate == prev:
                continue
            cx, cy = candidate
            if cx < 0 or cx >= self.width or cy < 0 or cy >= self.height:
                continue
            if self.ignore_slopes:
                if self.data[cy][cx] != "#":
                    neighbours.add(candidate)
            else:
                if self.data[cy][cx] == ".":
                    neighbours.add(candidate)
                elif self.data[cy][cx] != "#" and get_direction(point, candidate) == ARROW_TO_DIRECTION[self.data[cy][cx]]:
                    neighbours.add(candidate)
        return neighbours

    def get_path(self, start: Tuple[int, int], prev: Tuple[int, int] | None) -> Path:
        elements = list()
        elements.append(start)

        for el in self._get_neighbours(start, prev):
            if el != prev:
                elements.append(el)
                break

        while True:
            end = elements[-1]
            neighbours = self._get_neighbours(end, elements[-2])
            if len(neighbours) == 0:
                return Path(start, end, len(elements))
            elif len(neighbours) == 1:
                elements.append(neighbours.pop())
            else:
                return Path(start, end, len(elements), neighbours)

    def explore(self):
        paths = dict()
        current = {(None, self.source)}
        while len(current) > 0:
            prev, start = current.pop()
            path = self.get_path(start, prev)
            paths[start] = path
            for el in path.conjunctions:
                if el in paths:
                    continue
                current.add((path.end, el))
        return paths

    def _get_max_possible_length(self):
        total_length = 0
        for line in self.data:
            for el in line:
                if el != "#":
                    total_length += 1
        return total_length

    def get_required(self, paths, points):
        required = set()
        for source, path in paths.items():
            if len(path.conjunctions & points) > 0:
                required.add(path.start)
        return required

    def get_longest_hike(self):
        paths = self.explore()

        final_conjunction = None
        for source, path in paths.items():
            if path.end == self.target:
                final_conjunction = source
                break

        required = list()
        required.append({final_conjunction})
        for _ in range(4):
            r = self.get_required(paths, required[-1])
            required.append(r)

        assert final_conjunction is not None

        current = collections.deque()
        current.append((self.source, 0, set(), set()))
        max_length = -1
        while len(current) > 0:
            point, length, prev_conjunctions, removed_conjunctions = current.pop()
            path = paths[point]
            current_length = length + path.length
            if path.start in prev_conjunctions or path.end in prev_conjunctions:
                continue

            skip = False
            for possibilities_req in required:
                if len(possibilities_req - removed_conjunctions) == 0:
                    skip = True
                    break
            if skip:
                continue

            prev_conjunctions.add(path.start)
            prev_conjunctions.add(path.end)

            # Check if we got to the end
            if final_conjunction in path.conjunctions:
                path_length = current_length + paths[final_conjunction].length
                max_length = max(max_length, path_length - 1)
                continue

            for conjunction in path.conjunctions:
                new_conjunctions = prev_conjunctions.copy()
                new_rem_conjunctions = removed_conjunctions.copy()
                new_rem_conjunctions.update(path.conjunctions)
                new_rem_conjunctions.remove(conjunction)
                current.append((conjunction, length + path.length, new_conjunctions, new_rem_conjunctions))
        return max_length

    def solve1(self):
        return self.get_longest_hike()

    def solve2(self):
        self.ignore_slopes = True
        return self.get_longest_hike()


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
