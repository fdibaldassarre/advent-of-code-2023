#!/usr/bin/env python
import functools

MIRROR_MAPPINGS = {
    "/": {
        (1, 0): (0, -1),
        (-1, 0): (0, 1),
        (0, -1): (1, 0),
        (0, 1): (-1, 0)
    },
    "\\": {
        (1, 0): (0, 1),
        (-1, 0): (0, -1),
        (0, 1): (1, 0),
        (0, -1): (-1, 0)
    }
}


def move_towards(point, direction):
    x, y = point
    dx, dy = direction
    return x + dx, y + dy


class Solver:

    def __init__(self):
        self.data = None
        self.height = 0
        self.width = 0

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                self.data.append(line)
        self.height = len(self.data)
        self.width = len(self.data[0])

    @functools.lru_cache(maxsize=None)
    def _get_beam_exploration(self, initial_beam):
        height = len(self.data)
        width = len(self.data[0])

        explored = set()
        new_beams = set()
        current_beam = initial_beam
        while True:
            if current_beam in explored:
                break
            explored.add(current_beam)

            current_pos, current_dir = current_beam
            new_x, new_y = move_towards(current_pos, current_dir)
            if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
                break

            new_beams = set()
            point = self.data[new_y][new_x]
            if point == ".":
                current_beam = ((new_x, new_y), current_dir)
                continue
            # Break
            if point in MIRROR_MAPPINGS:
                new_direction = MIRROR_MAPPINGS[point][current_dir]
                new_beam = ((new_x, new_y), new_direction)
                new_beams.add(new_beam)
            elif point == "-":
                if current_dir[1] == 0:
                    new_beam = ((new_x, new_y), current_dir)
                    new_beams.add(new_beam)
                else:
                    beam_1 = ((new_x, new_y), (1, 0))
                    beam_2 = ((new_x, new_y), (-1, 0))
                    new_beams.add(beam_1)
                    new_beams.add(beam_2)
            elif point == "|":
                if current_dir[0] == 0:
                    new_beam = ((new_x, new_y), current_dir)
                    new_beams.add(new_beam)
                else:
                    beam_1 = ((new_x, new_y), (0, 1))
                    beam_2 = ((new_x, new_y), (0, -1))
                    new_beams.add(beam_1)
                    new_beams.add(beam_2)
            break

        points = set()
        for beam in explored:
            point, _ = beam
            points.add(point)

        return points, new_beams

    def _get_tiles_explored(self, initial_beam):
        beams = {initial_beam}
        points = set()
        explored = set()
        while len(beams) > 0:
            beam = beams.pop()
            if beam in explored:
                continue
            beam_points, new_beams = self._get_beam_exploration(beam)
            points.update(beam_points)
            beams.update(new_beams)
            explored.add(beam)
        return len(points) - 1

    def solve1(self):
        return self._get_tiles_explored(((-1, 0), (1, 0)))

    def solve2(self):
        best_result = 0
        # TOP-DOWN
        direction_down = (0, 1)
        direction_up = (0, -1)
        for x in range(self.width):
            result = self._get_tiles_explored(((x, -1), direction_down))
            best_result = max(best_result, result)
            result = self._get_tiles_explored(((x, self.height), direction_up))
            best_result = max(best_result, result)
        # LEFT-RIGHT
        direction_right = (1, 0)
        direction_left = (-1, 0)
        for y in range(self.height):
            result = self._get_tiles_explored(((-1, y), direction_right))
            best_result = max(best_result, result)
            result = self._get_tiles_explored(((self.width, y), direction_left))
            best_result = max(best_result, result)
        return best_result


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
