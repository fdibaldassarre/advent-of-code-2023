#!/usr/bin/env python
from typing import Tuple, List, Iterable

DIRECTIONS = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0)
}

NUMBER_TO_DIRECTION = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}


def get_extremes(points):
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    for point in points:
        x, y = point
        max_x = max(max_x, x)
        min_x = min(min_x, x)
        max_y = max(max_y, y)
        min_y = min(min_y, y)

    return (min_x, min_y), (max_x, max_y)


def decode(color: str) -> Tuple[str, int]:
    stride = color[:-1]
    direction = color[-1]
    return NUMBER_TO_DIRECTION[direction], int(stride, 16)


def print_trench(points):
    (min_x, min_y), (max_x, max_y) = get_extremes(points)

    trench_map = list()
    for y in range(min_y, max_y+1):
        line = ['.'] * (max_x - min_x + 1)
        trench_map.append(line)

    for point in points:
        x, y = point
        x -= min_x
        y -= min_y
        trench_map[y][x] = "#"

    trench_map[9][2] = "X"

    print(
        "\n".join("".join(line) for line in trench_map)
    )


def vector_sum(a: Iterable[int], b: Iterable[int]) -> Tuple[int, ...]:
    return tuple(a1 + b1 for a1, b1 in zip(a, b))
    #return tuple(a[i] + b[i] for i in range(len(a)))


def scalar_prod(a: int, v: List[int]) -> List[int]:
    return [a * el for el in v]


def get_neighbours(point):
    x, y = point
    yield x - 1, y
    yield x + 1, y
    yield x, y - 1
    yield x, y + 1


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                direction, meters, color = line.split(" ")
                meters = int(meters)
                color = color[2:-1]
                self.data.append((direction, meters, color))

    def _get_content_slow(self, trench):
        (min_x, min_y), (max_x, max_y) = get_extremes(trench)
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) in trench:
                    inside = (x + 1, y - 1)
                    break
        border = {inside}
        lagoon = set()
        while len(border) > 0:
            current = border.pop()
            if current in lagoon:
                continue
            lagoon.add(current)
            for point in get_neighbours(current):
                if point not in trench:
                    border.add(point)
        return len(lagoon) + len(trench)

    def get_vertices(self, movements: List[Tuple[str, int]]) -> List[Tuple[int, int]]:
        vertices = set()
        current = (0, 0)
        vertices.add(current)
        for movement in movements:
            direction, stride = movement
            direction_v = DIRECTIONS[direction]
            direction_v = scalar_prod(stride, direction_v)
            current = vector_sum(current, direction_v)
            vertices.add(current)
        vertices = list(vertices)
        vertices.sort()
        return vertices

    def _get_content_fast(self, vertices) -> int:
        # Split by levels
        levels = dict()
        for vertex in vertices:
            x, y = vertex
            if x not in levels:
                levels[x] = list()
            levels[x].append(y)
        for level in levels.values():
            level.sort()

        current_cubes = list()
        prev_x = None
        lagoon = 0
        for x, level in levels.items():
            # Increase size
            if prev_x is not None:
                height = x - prev_x
                for section in current_cubes:
                    lagoon += (section[1] - section[0] + 1) * height
            # Get new sections
            for i in range(len(level) // 2):
                section = [level[2*i], level[2*i + 1]]
                current_cubes.append(section)
            current_cubes.sort()
            # Merge and subtract
            new_cubes = list()
            for cube in current_cubes:
                current_start, current_end = cube
                if len(new_cubes) == 0:
                    new_cubes.append([current_start, current_end])
                    continue
                prev_start, prev_end = new_cubes[-1]
                if current_start > prev_end:
                    new_cubes.append([current_start, current_end])
                elif current_start == prev_end:
                    new_cubes[-1][1] = current_end
                else:
                    # current_start < prev_end
                    new_cubes.pop()
                    if prev_end < current_end:
                        prev_end, current_end = current_end, prev_end
                    added = 0
                    if current_start > prev_start:
                        new_cubes.append([prev_start, current_start])
                        added += 1
                    if prev_end > current_end:
                        new_cubes.append([current_end, prev_end])
                        added += 1
                    lagoon += (current_end - current_start - added + 1)
            current_cubes = new_cubes
            prev_x = x

        return lagoon

    def solve1(self):
        current = (0, 0)
        trench = {current}
        for movement in self.data:
            direction, meters, _ = movement
            direction_v = DIRECTIONS[direction]
            for _ in range(meters):
                current = vector_sum(current, direction_v)
                trench.add(current)
        return self._get_content_slow(trench)

    def solve2(self):
        movements = list()
        for movement in self.data:
            _, _, color = movement
            direction, meters = decode(color)
            movements.append((direction, meters))
        vertices = self.get_vertices(movements)
        return self._get_content_fast(vertices)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
