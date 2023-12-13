#!/usr/bin/env python

class Pattern:

    def __init__(self, pattern):
        self.pattern = pattern
        self.height = len(pattern)
        self.width = len(pattern[0])

    def iter_column(self, column):
        for row in self.pattern:
            yield row[column]

    def iter_columns(self):
        for column in range(self.width):
            yield list(self.iter_column(column))

    def is_symmetric(self, elements, idx):
        idx_left, idx_right = idx, idx + 1
        while 0 <= idx_left and idx_right < len(elements):
            if elements[idx_left] != elements[idx_right]:
                return False
            idx_left -= 1
            idx_right += 1
        return True

    def is_symmetric_with_smudge(self, elements, idx):
        idx_left, idx_right = idx, idx + 1
        smudge_used = False
        while 0 <= idx_left and idx_right < len(elements):
            if elements[idx_left] != elements[idx_right]:
                if smudge_used:
                    return False
                else:
                    smudge_used = True
            idx_left -= 1
            idx_right += 1
        return True

    def get_horizonal_split(self):
        possible_splits = list(range(self.height - 1))
        for column in self.iter_columns():
            new_splits = list()
            for split in possible_splits:
                if self.is_symmetric(column, split):
                    new_splits.append(split)
            possible_splits = new_splits
            if len(possible_splits) == 0:
                break
        return possible_splits[0] if len(possible_splits) > 0 else None

    def get_horizonal_split_with_smudge(self):
        possible_splits = list()
        for row in range(self.height - 1):
            possible_splits.append((row, False))

        for column in self.iter_columns():
            new_splits = list()
            for split_with_smudge in possible_splits:
                split, has_smudge = split_with_smudge
                if self.is_symmetric(column, split):
                    new_splits.append((split, has_smudge))
                elif not has_smudge and self.is_symmetric_with_smudge(column, split):
                    new_splits.append((split, True))
            possible_splits = new_splits
            if len(possible_splits) == 0:
                break

        splits_with_smudge = list()
        for split_with_smudge in possible_splits:
            split, has_smudge = split_with_smudge
            if has_smudge:
                splits_with_smudge.append(split)
        return splits_with_smudge[0] if len(splits_with_smudge) > 0 else None

    def get_vertical_split(self):
        possible_splits = list(range(self.width - 1))
        for row in self.pattern:
            new_splits = list()
            for split in possible_splits:
                if self.is_symmetric(row, split):
                    new_splits.append(split)
            possible_splits = new_splits
            if len(possible_splits) == 0:
                break
        return possible_splits[0] if len(possible_splits) > 0 else None

    def get_vertical_split_with_smudge(self):
        possible_splits = list()
        for column in range(self.width - 1):
            possible_splits.append((column, False))

        for row in self.pattern:
            new_splits = list()
            for split_with_smudge in possible_splits:
                split, has_smudge = split_with_smudge
                if self.is_symmetric(row, split):
                    new_splits.append((split, has_smudge))
                elif not has_smudge and self.is_symmetric_with_smudge(row, split):
                    new_splits.append((split, True))
            possible_splits = new_splits
            if len(possible_splits) == 0:
                break

        splits_with_smudge = list()
        for split_with_smudge in possible_splits:
            split, has_smudge = split_with_smudge
            if has_smudge:
                splits_with_smudge.append(split)
        return splits_with_smudge[0] if len(splits_with_smudge) > 0 else None


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            current = list()
            for line in hand:
                line = line.strip()
                if line == "":
                    self.data.append(current)
                    current = list()
                else:
                    current.append(line)
            if len(current) > 0:
                self.data.append(current)

    def solve1(self):
        result = 0
        for pattern in self.data:
            p = Pattern(pattern)
            split_v = p.get_vertical_split()
            if split_v is not None:
                result += (split_v + 1)
            split_h = p.get_horizonal_split()
            if split_h is not None:
                result += 100 * (split_h + 1)
        return result

    def solve2(self):
        result = 0
        for pattern in self.data:
            p = Pattern(pattern)
            split_v = p.get_vertical_split_with_smudge()
            if split_v is not None:
                result += (split_v + 1)
            split_h = p.get_horizonal_split_with_smudge()
            if split_h is not None:
                result += 100 * (split_h + 1)
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
