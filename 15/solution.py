#!/usr/bin/env python
import collections


class Box:
    """A box that preserves order-insertion
    (same as a dict in modern python actually XD)"""

    class BoxItem:

        def __init__(self, label, focal_power):
            self.label = label
            self.focal_power = focal_power
            self.prev = None
            self.next = None

        def update(self, focal_power):
            self.focal_power = focal_power

        def append(self, item: 'Box.BoxItem'):
            self.next = item
            if item is not None:
                item.prev = self

    def __init__(self):
        self.key_to_item = dict()
        self.first = Box.BoxItem(None, None)
        self.last = self.first

    def __getitem__(self, item):
        box_item = self.key_to_item.get(item)
        return box_item.focal_power if box_item is not None else None

    def __setitem__(self, key, value):
        existing = self.key_to_item.get(key)
        if existing is None:
            # Add item
            existing = Box.BoxItem(key, value)
            self.key_to_item[key] = existing
            self.last.append(existing)
            self.last = existing
        else:
            existing.update(value)

    def __delitem__(self, key):
        existing = self.key_to_item.get(key)
        if existing is not None:
            del self.key_to_item[key]
            prev_item = existing.prev
            next_item = existing.next
            prev_item.append(next_item)
            if next_item is None:
                self.last = prev_item

    def __contains__(self, item):
        return item in self.key_to_item

    def keys(self):
        current = self.first.next
        while current is not None:
            yield current.label
            current = current.next


class BoxMap:

    def __init__(self):
        self.boxes = [
            Box() for _ in range(256)
            # dict() for _ in range(256)
        ]

    def remove_lens(self, box_id, label):
        box = self.boxes[box_id]
        if label in box:
            del box[label]

    def add_lens(self, box_id, label, focal_pow):
        box = self.boxes[box_id]
        box[label] = focal_pow

    def get_focusing_power(self):
        power = 0
        for i, box in enumerate(self.boxes):
            box_id = i + 1
            for j, lens in enumerate(box.keys()):
                lens_id = j + 1
                power += box_id * lens_id * box[lens]
        return power


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        with open(file) as hand:
            line = hand.readline().strip()
            self.data = line.split(",")

    def _compute_HASH(self, value: str) -> int:
        current = 0
        for ch in value:
            current += ord(ch)
            current *= 17
            current = current % 256
        return current

    def solve1(self):
        result = 0
        for el in self.data:
            result += self._compute_HASH(el)
        return result

    def solve2(self):
        box_map = BoxMap()
        for el in self.data:
            if "-" in el:
                label = el[:-1]
                code = self._compute_HASH(label)
                box_map.remove_lens(code, label)
            else:
                label, focal_pow = el.split("=")
                code = self._compute_HASH(label)
                focal_pow = int(focal_pow)
                box_map.add_lens(code, label, focal_pow)

        return box_map.get_focusing_power()


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
