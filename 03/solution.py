#!/usr/bin/env python

class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                self.data.append(line)

    def get_numbers(self):
        N = len(self.data)
        M = len(self.data[0])
        for i in range(N):
            line = self.data[i]
            j = 0
            while j < M:
                while j < M and not str.isdigit(line[j]):
                    j += 1
                if j == M:
                    break
                digit_start = j
                digit_end = j + 1
                while digit_end < M and str.isdigit(line[digit_end]):
                    digit_end += 1
                yield i, (digit_start, digit_end)
                j = digit_end

    def is_symbol(self, character):
        return character != "." and not str.isdigit(character)

    def get_adjacent_symbols(self, x, y_start, y_end):
        line_idx_start = max(0, y_start - 1)
        line_idx_end = min(y_end, len(self.data) - 1)
        if self.is_symbol(self.data[x][line_idx_start]):
            yield x, line_idx_start
        if self.is_symbol(self.data[x][line_idx_end]):
            yield x, line_idx_end
        for data_idx in [max(0, x - 1), min(len(self.data) - 1, x + 1)]:
            for line_idx in range(line_idx_start, line_idx_end + 1):
                if self.is_symbol(self.data[data_idx][line_idx]):
                    yield data_idx, line_idx

    def is_adjacent_symbol(self, x, y_start, y_end):
        for _ in self.get_adjacent_symbols(x, y_start, y_end):
            return True
        return False

    def get_adjacent_stars(self, x, y_start, y_end):
        for symbol_x, symbol_y in self.get_adjacent_symbols(x, y_start, y_end):
            if self.data[symbol_x][symbol_y] == "*":
                yield symbol_x, symbol_y

    def get_gears(self):
        stars_with_numbers = dict()
        for number_at_position in self.get_numbers():
            i, position = number_at_position
            number = int(self.data[i][position[0]:position[1]])
            for star_pos in self.get_adjacent_stars(i, *position):
                if star_pos not in stars_with_numbers:
                    stars_with_numbers[star_pos] = list()
                stars_with_numbers[star_pos].append(number)
        return {pos: numbers
                for pos, numbers in stars_with_numbers.items()
                if len(numbers) == 2
                }

    def solve1(self):
        result = 0
        for number_at_position in self.get_numbers():
            i, position = number_at_position
            number = self.data[i][position[0]:position[1]]
            if self.is_adjacent_symbol(i, *position):
                result += int(number)
        return result

    def solve2(self):
        result = 0
        for gear, numbers in self.get_gears().items():
            ratio = numbers[0] * numbers[1]
            result += ratio
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
