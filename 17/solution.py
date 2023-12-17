#!/usr/bin/env python
import heapq
from typing import Tuple


DIRECTION_TO_STR = {
    (1, 0): ">",
    (-1, 0): "<",
    (0, 1): "V",
    (0, -1): "^"
}


def min_null_safe(a: int | None, b: int | None) -> int:
    if a is None:
        return b
    if b is None:
        return a
    return min(a, b)


class Status:

    def __init__(self, point: Tuple[int, int], heat_loss: int, strait_steps: int,
                 direction: Tuple[int, int], previous: 'Status' = None):
        self.point = point
        self.heat_loss = heat_loss
        self.strait_steps = strait_steps
        self.direction = direction
        self._prev = previous

    def values(self):
        return self.point, self.heat_loss, self.strait_steps, self.direction

    def print(self):
        item = self
        max_x, max_y = self.point
        data = list()
        for _ in range(max_y + 1):
            data.append([' '] * (max_x + 1))
        while item is not None:
            x, y = item.point
            data[y][x] = DIRECTION_TO_STR.get(item.direction)
            item = item._prev

        print("\n".join(
            "".join(line) for line in data
        ))


class StatusQueue:

    def __init__(self, target: Tuple[int, int]):
        self.queue = list()
        self.target_x, self.target_y = target
        self._count = 0
        heapq.heapify(self.queue)

    def _get_priority(self, item: Status) -> int:
        point, heat_loss, _, _ = item.values()
        x, y = point
        expected_loss_score = self.target_x - x + self.target_y - y + heat_loss
        return expected_loss_score

    def pop(self) -> Tuple[int, Status]:
        min_final_heat_loss, _, item = heapq.heappop(self.queue)
        return min_final_heat_loss, item

    def add(self, item: Status) -> None:
        prio = self._get_priority(item)
        counter = self._count
        self._count += 1
        heapq.heappush(self.queue, (prio, counter, item))

    def __len__(self) -> int:
        return len(self.queue)


class ExploredPoints:

    def __init__(self, use_ultra_crucible: bool):
        self.explored = dict()
        self.use_ultra_crucible = use_ultra_crucible
        self.max_steps = 3 if not use_ultra_crucible else 10

    def mark_explored(self, status: Status) -> bool:
        point, heat_loss, strait_steps, direction = status.values()
        if point not in self.explored:
            self.explored[point] = {
                (1, 0): [None] * (self.max_steps + 1),
                (-1, 0): [None] * (self.max_steps + 1),
                (0, 1): [None] * (self.max_steps + 1),
                (0, -1): [None] * (self.max_steps + 1),
            }
        costs = self.explored[point][direction]
        explored_cost = costs[strait_steps]
        if explored_cost is not None and explored_cost <= heat_loss:
            # Already explored
            return True

        # Update explored values
        if not self.use_ultra_crucible:
            for steps in range(strait_steps, 4):
                costs[steps] = min_null_safe(heat_loss, costs[steps])
        else:
            costs[strait_steps] = min_null_safe(heat_loss, costs[strait_steps])

        return False


class Solver:

    def __init__(self):
        self.data = None
        self.width = 0
        self.height = 0

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                line = list(map(int, line))
                self.data.append(line)
        self.width = len(self.data[0])
        self.height = len(self.data)

    def _is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def _get_directions(self, point, strait_steps, direction, use_ultra_crucible):
        x, y = point
        dx, dy = direction
        max_steps_straight = 3 if not use_ultra_crucible else 10
        if strait_steps < max_steps_straight:
            new_x, new_y = x + dx, y + dy
            if self._is_valid(new_x, new_y):
                yield (new_x, new_y), direction
        min_steps_turn = 0 if not use_ultra_crucible else 4
        if strait_steps >= min_steps_turn:
            # Left
            new_x, new_y = x + dy, y - dx
            if self._is_valid(new_x, new_y):
                yield (new_x, new_y), (dy, -dx)
            # Right
            new_x, new_y = x - dy, y + dx
            if self._is_valid(new_x, new_y):
                yield (new_x, new_y), (-dy, dx)

    def _solve(self, use_ultra_crucible: bool):
        target = (self.width - 1, self.height - 1)
        positions = StatusQueue(target)
        for starting_direction in [(1, 0), (0, 1)]:
            positions.add(Status((0, 0), 0, 0, starting_direction))
        best_result = None
        best_solution = None
        explored = ExploredPoints(use_ultra_crucible)
        while len(positions) > 0:
            best_possible_heat_loss, current = positions.pop()
            point, heat_loss, strait_steps, direction = current.values()
            if point == target:
                # Arrived at target
                if use_ultra_crucible and strait_steps < 4:
                    # Invalid solution
                    continue
                best_result = min_null_safe(best_result, heat_loss)
                if heat_loss == best_result:
                    best_solution = current
                continue
            if best_result is not None and best_possible_heat_loss >= best_result:
                # Too much heat loss
                continue
            if explored.mark_explored(current):
                # Point was already explored with better status
                continue
            # Get new directions
            for block_and_direction in self._get_directions(point, strait_steps, direction, use_ultra_crucible):
                new_point, new_direction = block_and_direction
                new_x, new_y = new_point
                new_loss = heat_loss + self.data[new_y][new_x]
                new_strait_steps = strait_steps
                if new_direction == direction:
                    new_strait_steps += 1
                else:
                    new_strait_steps = 1
                positions.add(Status(new_point, new_loss, new_strait_steps, new_direction, previous=current))

        # best_solution.print()
        return best_result

    def solve1(self):
        return self._solve(use_ultra_crucible=False)

    def solve2(self):
        return self._solve(use_ultra_crucible=True)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
