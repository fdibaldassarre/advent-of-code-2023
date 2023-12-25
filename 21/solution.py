#!/usr/bin/env python


class Solver:

    def __init__(self):
        self.data = None
        self.start = None
        self.height = 0
        self.width = 0

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                self.data.append(line)
                if "S" in line:
                    self.start = (line.index("S"), len(self.data) - 1)
        self.height = len(self.data)
        self.width = len(self.data[0])

    def _get_neighbours(self, point):
        x, y = point
        for point in [
            (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)
        ]:
            new_x, new_y = point
            if 0 <= new_x < self.width and 0 <= new_y < self.height and self.data[new_y][new_x] != "#":
                yield point

    def explore(self, start):
        point_to_min_steps = {
            start: 0,
        }
        current = {start}
        steps = 0
        n_even = 1
        n_odd = 0
        while len(current) > 0:
            steps += 1
            new_values = set()
            for el in current:
                for point in self._get_neighbours(el):
                    if point in point_to_min_steps:
                        continue
                    point_to_min_steps[point] = steps
                    if steps % 2 == 0:
                        n_even += 1
                    else:
                        n_odd += 1
                    new_values.add(point)
            current = new_values
        return n_even, n_odd

    def get_even_odd_maps(self, tot_steps):
        side_explored = (tot_steps - 2 * self.width) // self.width

        if side_explored == 0:
            return 0, 0, 0, 0

        total_width = 2 * side_explored - 1
        odd_on_zero_line = 2 * (total_width // 4) + 1

        odd_squares = int(odd_on_zero_line ** 2)
        total_squares = (total_width + 1) ** 2 // 2 - total_width

        even_squares = total_squares - odd_squares
        return side_explored, total_width, even_squares, odd_squares

    def get_reachable(self, start, steps):
        current = {start}
        for _ in range(steps):
            new_values = set()
            for el in current:
                for point in self._get_neighbours(el):
                    new_values.add(point)
            current = new_values
            if len(current) == 0:
                break
        return current

    def count_reachable(self, points_with_steps):
        reachable = set()
        for point, steps in points_with_steps.items():
            if steps >= 0:
                new_reach = self.get_reachable(point, steps)
                reachable.update(new_reach)

        return len(reachable)

    def get_diagonal_steps(self, side_maps, steps):
        points = [
            (0, 0), (self.width - 1, 0), (self.width - 1, self.height - 1), (0, self.height - 1)
        ]
        border_steps = 0
        for point in points:
            border_steps += side_maps * self.count_reachable({point: steps})
        return border_steps

    def get_border_steps(self, max_maps_traversed, rem_steps_on_side, rem_steps_on_corner):
        border_steps = 0
        side_points = [
            [(0, 0), (self.width // 2, 0), (self.width - 1, 0)],
            [(self.width - 1, 0), (self.width - 1, self.height // 2), (self.width - 1, self.height - 1)],
            [(self.width - 1, self.height - 1), (self.width // 2, self.height - 1), (0, self.height - 1)],
            [(0, self.height - 1), (0, self.height // 2), (0, 0)],
        ]

        for side_point in side_points:
            dx = dict()
            dx[side_point[0]] = rem_steps_on_corner - 1
            dx[side_point[1]] = rem_steps_on_side - 1
            dx[side_point[2]] = rem_steps_on_corner - 1
            border_steps += self.count_reachable(dx)

        border_steps += self.get_diagonal_steps(max_maps_traversed - 1, rem_steps_on_corner - 2)

        return border_steps

    def solve1(self):
        return self.count_reachable({self.start: 64})

    def solve2(self):
        tot_steps = 26501365
        n_even, n_odd = self.explore(self.start)
        side_explored, total_width, even_maps, odd_maps = self.get_even_odd_maps(tot_steps)

        explored = even_maps * n_even + odd_maps * n_odd

        steps_used_on_side = self.width // 2 + ((side_explored - 1) * self.width)
        steps_used_on_corner = self.width - 1 + ((side_explored - 1) * self.width)

        rem_side_steps = tot_steps - steps_used_on_side
        rem_corner_steps = tot_steps - steps_used_on_corner

        explored += self.get_diagonal_steps(side_explored - 1, rem_corner_steps + self.width - 2)

        while rem_side_steps > 0:
            side_explored += 1
            explored += self.get_border_steps(side_explored, rem_side_steps, rem_corner_steps)
            rem_side_steps -= self.width
            rem_corner_steps -= self.width

        return explored


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
