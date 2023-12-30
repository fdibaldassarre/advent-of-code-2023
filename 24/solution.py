#!/usr/bin/env python
import collections
import math
from typing import Tuple, List, Set

from modint import ChineseRemainderConstructor


def factorize(n: int) -> List[int]:
    res = [1]
    for c in range(2, int(n ** 0.5)):
        if n % c == 0:
            res.append(c)
            res.append(n // c)
    res.append(n)
    return res


def vector_sum(*points: Tuple[int, ...]) -> Tuple[int, ...]:
    result = [0] * len(points[0])
    for point in points:
        for i in range(len(result)):
            result[i] += point[i]
    return tuple(result)


def dot_prod(n: int, point: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(n * i for i in point)


class HailstoneTrajectory:

    def __init__(self, start, speed, line_xy, line_xz, plane_x):
        self.start = start
        self.speed = speed
        self.line_xy = line_xy
        self.line_xz = line_xz
        self.plane_x = plane_x

    def get_line(self) -> Tuple[float, float]:
        return self.line_xy

    def get_line_z(self):
        return self.line_xz

    def is_in_future(self, x: float) -> bool:
        if self.plane_x[0] is None:
            return x <= self.plane_x[1]
        else:
            return x >= self.plane_x[0]

    def get_at(self, time: int) -> Tuple[int, int, int]:
        return vector_sum(self.start, dot_prod(time, self.speed))


def get_line2d(point: Tuple[int, int], speed: Tuple[int, int]) -> Tuple[float, float]:
    a, b = speed
    m = b / a
    r, s = point
    q = s - m * r
    return m, q


def get_trajectory_between(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> HailstoneTrajectory:
    s = vector_sum(p2, dot_prod(-1, p1))
    return get_trajectory(p1, s)


def get_trajectory(point: Tuple[int, int, int], speed: Tuple[int, int, int]) -> HailstoneTrajectory:
    line_xy = get_line2d((point[0], point[1]), (speed[0], speed[1]))
    line_xz = get_line2d((point[0], point[2]), (speed[0], speed[2]))
    if speed[0] > 0:
        plane_x = [point[0], None]
    else:
        plane_x = [None, point[0]]
    return HailstoneTrajectory(point, speed, line_xy, line_xz, plane_x)


def get_intersection(trajectory1: HailstoneTrajectory, trajectory2: HailstoneTrajectory) -> Tuple[float, float] | None:
    m1, q1 = trajectory1.get_line()
    m2, q2 = trajectory2.get_line()
    if m1 == m2:
        return None
    x = (q2 - q1) / (m1 - m2)
    if not trajectory1.is_in_future(x) or not trajectory2.is_in_future(x):
        return None
    y = m1 * x + q1
    return x, y


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                point, speed = line.split(" @ ")
                point = tuple(map(int, point.split(", ")))
                speed = tuple(map(int, speed.split(", ")))
                self.data.append((point, speed))

    def solve1(self):
        test_area = [200000000000000, 400000000000000]

        trajectories = list()
        for point, speed in self.data:
            trajectories.append(get_trajectory(point, speed))

        result = 0
        for i, trajectory in enumerate(trajectories):
            for j in range(i + 1, len(trajectories)):
                intersection = get_intersection(trajectory, trajectories[j])
                if intersection is not None:
                    valid = True
                    for coord in intersection:
                        if coord < test_area[0] or coord > test_area[1]:
                            valid = False
                            break
                    if valid:
                        result += 1

        return result

    def get_parallel_and_extra(self, trajectories) -> Tuple[HailstoneTrajectory, HailstoneTrajectory, HailstoneTrajectory]:
        coeffs = dict()
        parallel = None
        for trajectory in trajectories:
            if parallel is not None:
                return parallel[0], parallel[1], trajectory
            m = trajectory.get_line()[0]
            if parallel is None and m in coeffs:
                parallel = coeffs[m], trajectory
            coeffs[m] = trajectory

    def _get_possible_speeds(self, common_speed: int, axis: int) -> Set[int]:
        d = list()
        for point, speed in self.data:
            if speed[axis] == common_speed:
                d.append(point[axis])

        s = list()
        for i in range(1, len(d)):
            s.append(abs(d[i] - d[0]))

        factors = factorize(math.gcd(*s))
        possible_v = set()
        for f in factors:
            possible_v.add(abs(f + common_speed))
            possible_v.add(abs(f - common_speed))
        return possible_v

    def _get_speed(self, axis: int) -> int:
        point_speeds = list()
        for _, speed in self.data:
            point_speeds.append(speed[axis])
        counter = collections.Counter(point_speeds)
        common_speeds = counter.most_common(n=4)
        possible_speeds = (self._get_possible_speeds(common_speeds[0][0], axis=axis)
                           &
                           self._get_possible_speeds(common_speeds[1][0], axis=axis)
                           &
                           self._get_possible_speeds(common_speeds[2][0], axis=axis)
                           &
                           self._get_possible_speeds(common_speeds[3][0], axis=axis)
                           )
        assert len(possible_speeds) == 1
        return possible_speeds.pop()

    def _add_equation(self, pairs, v, r):
        not_coprime = None
        for k in pairs.keys():
            if math.gcd(k, v) > 1:
                not_coprime = k
                break
        if not_coprime is None:
            pairs[v] = r

    def _get_start_pairs(self, used_speed: int, axis: int):
        pairs = dict()
        for point, speed in self.data:
            v = abs(used_speed - speed[axis])
            r = point[axis] % v
            if v == 1:
                continue
            if v in pairs and pairs[v] != r:
                return None
            self._add_equation(pairs, v, r)
        return pairs

    def _get_start(self, common_speed, axis):
        # print("Axis", axis, "Speed on axis", common_speed[axis])
        pairs = self._get_start_pairs(common_speed[axis], axis=axis)
        if pairs is None:
            pairs = self._get_start_pairs(-1 * common_speed[axis], axis=axis)

        p = list()
        q = list()
        for base, value in pairs.items():
            p.append(base)
            q.append(value)
        chr = ChineseRemainderConstructor(p)
        return chr.rem(q)

    def solve2(self):

        speed_abs = list()
        for axis in range(3):
            speed_abs.append(self._get_speed(axis))

        points = list()
        for axis in range(3):
            points.append(self._get_start(speed_abs, axis=axis))

        return sum(points)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
