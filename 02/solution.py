#!/usr/bin/env python

class Solver:

    def __init__(self):
        self.data = None

    def _parse_extractions(self, raw_line):
        extractions = list()
        for extraction in raw_line.split("; "):
            single_extraction = dict()
            for num_and_color in extraction.split(", "):
                num, color = num_and_color.split(" ")
                num = int(num)
                single_extraction[color] = num
            extractions.append(single_extraction)
        return extractions

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                game_raw, sets_raw = line.split(": ")
                game_id = int(game_raw[len("Game "):])
                extractions = self._parse_extractions(sets_raw)
                self.data.append((game_id, extractions))

    def solve1(self):
        target = {
            "red": 12,
            "green": 13,
            "blue": 14
        }

        def are_all_possible(results):
            for extraction_res in results:
                for color, max_val in target.items():
                    extracted = extraction_res.get(color, 0)
                    if extracted > max_val:
                        return False
            return True

        result = 0
        for game_id, extractions in self.data:
            if are_all_possible(extractions):
                result += game_id
        return result

    def solve2(self):

        def get_min_cubes(game_extractions):
            res = {"red": 0, "green": 0, "blue": 0}
            for game_extraction in game_extractions:
                for color in res.keys():
                    res[color] = max(res[color], game_extraction.get(color, 0))
            return res

        result = 0
        for game_id, extractions in self.data:
            min_cubes = get_min_cubes(extractions)
            cubes_power = min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]
            result += cubes_power
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
