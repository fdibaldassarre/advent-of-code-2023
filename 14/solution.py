#!/usr/bin/env python

def _compact(data):
    return "\n".join(
            "".join(line) for line in data
        )


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                self.data.append(line)

    def _rotate_left(self, data):
        height = len(data)
        width = len(data[0])
        new_data = list()
        for x in range(width):
            new_data.append(["."] * height)

        for y in range(height):
            for x in range(width):
                new_y = width - x - 1
                new_x = y
                new_data[new_y][new_x] = data[y][x]

        return new_data

    def _rotate_right(self, data):
        height = len(data)
        width = len(data[0])
        new_data = list()
        for x in range(width):
            new_data.append(["."] * height)

        for y in range(height):
            for x in range(width):
                new_y = x
                new_x = height - y - 1
                new_data[new_y][new_x] = data[y][x]

        return new_data

    def _move_north(self, data):
        width = len(data[0])
        height = len(data)
        new_data = list()
        new_data.append([el for el in data[0]])
        min_free = [1] * width
        for i in range(width):
            if new_data[0][i] == ".":
                min_free[i] = 0
        for y in range(1, height):
            new_data.append(["."] * width)
            for x in range(width):
                if data[y][x] == "O":
                    y_free = min_free[x]
                    new_data[y][x] = "."
                    new_data[y_free][x] = "O"
                    min_free[x] += 1
                else:
                    new_data[y][x] = data[y][x]
                    if data[y][x] == "#":
                        min_free[x] = y + 1
        return new_data

    def _compute_load(self, data):
        total_load = 0
        for y, line in enumerate(data):
            for x in line:
                if x == "O":
                    load = len(data) - y
                    total_load += load
        return total_load

    def solve1(self):
        new_data = self._move_north(self.data)
        return self._compute_load(new_data)

    def spin(self, data):
        data = self._move_north(data)
        for _ in range(3):
            data = self._rotate_right(data)
            data = self._move_north(data)
        data = self._rotate_right(data)
        return data

    def solve2(self):
        data = self.data

        unique = dict()
        unique[_compact(data)] = 0
        loads = list()
        loads.append(self._compute_load(data))

        for i in range(1000000000):
            data = self.spin(data)
            encoded = _compact(data)
            if encoded in unique:
                base = unique[encoded]
                period = (i + 1) - unique[encoded]
                break
            unique[encoded] = i + 1
            loads.append(self._compute_load(data))

        n_required = (1000000000 - base) % period

        return loads[base + n_required]


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
