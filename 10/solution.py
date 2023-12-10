#!/usr/bin/env python

POINT_START = "S"
POINT_GROUND = "."
PIPE_NORTH_SOUTH = "|"
PIPE_EAST_WEST = "-"
PIPE_NORTH_EAST = "L"
PIPE_NORTH_WEST = "J"
PIPE_SOUTH_WEST = "7"
PIPE_SOUTH_EAST = "F"

WEST = (0, -1)
EAST = (0, 1)
NORTH = (-1, 0)
SOUTH = (1, 0)

PIPE_TO_DIRECTIONS = {
    "|": (NORTH, SOUTH),
    "-": (EAST, WEST),
    "L": (NORTH, EAST),
    "J": (NORTH, WEST),
    "7": (SOUTH, WEST),
    "F": (SOUTH, EAST)
}


def get_direction_wrt(x, y):
    return x[0] - y[0], x[1] - y[1]


def get_point_at(point, direction):
    return point[0] + direction[0], point[1] + direction[1]


def get_opposite(direction):
    return -1 * direction[0], -1 * direction[1]


def is_orthogonal(v1, v2):
    ps = v1[0] * v2[0] + v1[1] * v2[1]
    return ps == 0


def rotate_right(v):
    return -v[1], v[0]

def rotate_left(v):
    return v[1], -v[0]

class Navigator:

    def __init__(self, data):
        self.data = data

    def _go_along(self, point, direction):
        prev = point
        current = get_point_at(point, direction)
        pipe_type = self.data.get(current)
        if pipe_type is None or pipe_type == POINT_START or pipe_type == POINT_GROUND:
            return None
        incoming_direction = get_direction_wrt(prev, current)
        exit_directions = PIPE_TO_DIRECTIONS.get(pipe_type)

        if incoming_direction == exit_directions[0]:
            exit_direction = exit_directions[1]
        else:
            exit_direction = exit_directions[0]

        return current, exit_direction

    def get_pipes_connected_to_start(self, start):
        possible_directions = list()
        for direction in [NORTH, SOUTH, EAST, WEST]:
            candidate = get_point_at(start, direction)
            pipe_type = self.data.get(candidate)
            if pipe_type not in PIPE_TO_DIRECTIONS:
                continue
            valid_directions = PIPE_TO_DIRECTIONS[pipe_type]
            if get_opposite(direction) in valid_directions:
                target = get_direction_wrt(candidate, start)
                possible_directions.append(target)
        return possible_directions

    def navigate_loop(self, start):
        possible_directions = self.get_pipes_connected_to_start(start)
        points = [
            (start, possible_directions[0]),
            (start, possible_directions[1])
        ]
        while True:
            for i, status in enumerate(points):
                next_point, next_direction = self._go_along(*status)
                points[i] = (next_point, next_direction)
            yield points
            if points[0][0] == points[1][0]:
                break

    def get_loop(self, start):
        loop = list()
        possible_directions = self.get_pipes_connected_to_start(start)
        current = start
        current_direction = possible_directions[0]

        while True:
            loop.append(current)
            status = self._go_along(current, current_direction)
            if status is None:
                break
            current, current_direction = status
        return loop




class Solver:

    def __init__(self):
        self.data = None
        self.start = None
        self.max_x = -1
        self.max_y = -1

    def parse(self, file):
        self.data = dict()
        with open(file) as hand:
            for y, line in enumerate(hand):
                line = line.strip()
                self.max_y = max(self.max_y, y)
                self.max_x = len(line) - 1
                for x, el in enumerate(line):
                    self.data[(y, x)] = el
                    if el == POINT_START:
                        self.start = (y, x)

    def solve1(self):
        navigator = Navigator(self.data)
        distance = 0
        for _ in navigator.navigate_loop(self.start):
            distance += 1
        return distance

    def solve2(self):
        navigator = Navigator(self.data)
        loop = navigator.get_loop(self.start)
        loop_set = set(loop)

        start_idx = None
        inside_direction = None
        for y in range(self.max_y + 1):
            prev = (y, -1)
            for x in range(self.max_x + 1):
                if (y, x) in loop_set:
                    start_idx = loop.index((y, x))
                    outside_direction = get_direction_wrt(prev, (y, x))
                    inside_direction = get_opposite(outside_direction)
                    break
                prev = (y, x)
            if start_idx is not None:
                break

        # Get direction orthogonal to inside_direction
        direction = 1
        current_point = loop[start_idx]
        next_point = loop[(start_idx + direction) % len(loop)]
        loop_direction = get_direction_wrt(next_point, current_point)
        if not is_orthogonal(loop_direction, inside_direction):
            direction = -1
            next_point = loop[(start_idx + direction) % len(loop)]
            loop_direction = get_direction_wrt(next_point, current_point)
            #print("Next v2", next_point, inside_direction)

        inside_points = set()
        for dx in range(len(loop)):
            current_point = loop[(start_idx + direction * dx) % len(loop)]
            #print(current_point, self.data[current_point])
            inside_point = get_point_at(current_point, inside_direction)
            if inside_point not in loop_set:
                inside_points.add(inside_point)

            next_point = loop[(start_idx + direction * (dx + 1)) % len(loop)]
            next_loop_direction = get_direction_wrt(next_point, current_point)
            if next_loop_direction != loop_direction:
                # Rotate
                if next_loop_direction == rotate_right(loop_direction):
                    inside_direction = rotate_right(inside_direction)
                else:
                    inside_direction = rotate_left(inside_direction)
                inside_point = get_point_at(current_point, inside_direction)
                if inside_point not in loop_set:
                    inside_points.add(inside_point)
                # Go along
                loop_direction = next_loop_direction


        actual_inside = set()
        border = inside_points
        while len(border) > 0:
            point = border.pop()
            actual_inside.add(point)
            for direction in [NORTH, SOUTH, WEST, EAST]:
                new_point = get_point_at(point, direction)
                if self.data.get(new_point) is None:
                    continue
                if new_point not in loop_set and new_point not in actual_inside:
                    border.add(new_point)

        return len(actual_inside)




def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
