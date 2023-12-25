#!/usr/bin/env python
from typing import Tuple, List


class Cube:

    def __init__(self, start: Tuple[int, int, int], end: Tuple[int, int, int]):
        self.start = start
        self.end = end

    def get_distance_from_floor(self):
        return min(self.start[2], self.end[2]) - 1

    def get_horizontal_section(self) -> List[Tuple[int, int]]:
        s_x, s_y, _ = self.start
        e_x, e_y, _ = self.end
        values = list()
        for x in range(s_x, e_x + 1):
            for y in range(s_y, e_y + 1):
                values.append((x, y))
        return values

    def lower_at(self, z: int) -> 'Cube':
        s_x, s_y, s_z = self.start
        e_x, e_y, e_z = self.end
        min_z = min(s_z, e_z)
        assert z <= min_z
        dz = min_z - z
        return Cube((s_x, s_y, s_z - dz), (e_x, e_y, e_z - dz))

    def get_max_z(self) -> int:
        return max(self.start[2], self.end[2])


class Grid:
    def __init__(self, heights):
        self.heights = heights
        self.point_to_cube = dict()

    def add_cube(self, cube: Cube) -> Tuple[Cube, List[Cube]]:
        sustaining = set()
        max_z = 0
        for point in cube.get_horizontal_section():
            x, y = point
            z_occupied = self.heights[(x, y)]
            if z_occupied > max_z:
                max_z = z_occupied
                sustaining = set()
            if z_occupied == max_z:
                exiting_cube = self.point_to_cube.get(point)
                if exiting_cube is not None:
                    sustaining.add(exiting_cube)
        available_z = max_z + 1
        fallen_cube = cube.lower_at(available_z)
        occupied_z = fallen_cube.get_max_z()
        for point in fallen_cube.get_horizontal_section():
            self.heights[point] = occupied_z
            self.point_to_cube[point] = fallen_cube

        return fallen_cube, list(sustaining)

    @classmethod
    def build(cls, size_x, size_y):
        heights = dict()
        for x in range(size_x):
            for y in range(size_y):
                heights[(x, y)] = 0
        return Grid(heights)


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                start, end = line.split("~")
                start = tuple(map(int, start.split(",")))
                end = tuple(map(int, end.split(",")))
                self.data.append((start, end))

    def get_grid_size(self):
        max_x, max_y, max_z = 0, 0, 0
        for el in self.data:
            for point in el:
                x, y, z = point
                max_x = max(x, max_x)
                max_y = max(y, max_y)
                max_z = max(z, max_z)
        return max_x + 1, max_y + 1, max_z + 1

    def build_grid(self):
        size_x, size_y, _ = self.get_grid_size()
        return Grid.build(size_x, size_y)

    def get_falling_cubes(self):
        falling = list()
        for el in self.data:
            falling.append(Cube(*el))

        falling.sort(key=lambda c: c.get_distance_from_floor())
        return falling

    def let_the_cubes_fall(self):
        falling = self.get_falling_cubes()
        grid = self.build_grid()

        stable_cubes = set()
        cube_to_sustaining = dict()
        for cube in falling:
            fallen_cube, sustaining = grid.add_cube(cube)
            cube_to_sustaining[fallen_cube] = sustaining
            stable_cubes.add(fallen_cube)
        return stable_cubes, cube_to_sustaining

    def get_cubes_causing_falls(self, cube_to_sustaining):
        mandatory_cubes = set()
        for cube, sustaining in cube_to_sustaining.items():
            if len(sustaining) == 1:
                mandatory_cube = sustaining[0]
                mandatory_cubes.add(mandatory_cube)
        return mandatory_cubes

    def solve1(self):
        stable_cubes, cube_to_sustaining = self.let_the_cubes_fall()
        mandatory_cubes = self.get_cubes_causing_falls(cube_to_sustaining)

        candidates = stable_cubes - mandatory_cubes

        return len(candidates)

    def solve2(self):
        stable_cubes, cube_to_sustaining = self.let_the_cubes_fall()

        sustainer_to_cube = {cube: set() for cube in stable_cubes}
        for cube, sustaining in cube_to_sustaining.items():
            for sustainer in sustaining:
                sustainer_to_cube[sustainer].add(cube)

        mandatory_cubes = self.get_cubes_causing_falls(cube_to_sustaining)
        result = 0
        for cube in mandatory_cubes:
            falling = {cube}
            current = {cube}
            while len(current) > 0:
                new_current = set()
                for cube_falling in current:
                    for sustained in sustainer_to_cube[cube_falling]:
                        sustaining = set(cube_to_sustaining[sustained])
                        rem = sustaining - falling
                        if len(rem) == 0:
                            new_current.add(sustained)
                            falling.add(sustained)
                current = new_current
            result += len(falling) - 1

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
