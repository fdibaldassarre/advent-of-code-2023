#!/usr/bin/env python
import abc
import json
from typing import Dict, List, Tuple


def less_or_equal_null_safe(a, b):
    if a is None or b is None:
        return True
    return a <= b


def min_ignore_null(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return min(a, b)


def max_ignore_null(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return max(a, b)


def intersect_all(intervals1, intervals2):
    intersections = list()
    for interval in intervals1:
        for other in intervals2:
            # Start int
            start_int = max_ignore_null(other[0], interval[0])
            end_int = min_ignore_null(other[1], interval[1])
            if less_or_equal_null_safe(start_int, end_int):
                intersections.append((start_int, end_int))
    return intersections


class Condition:

    @abc.abstractmethod
    def is_always_false(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def eval(self, part: Dict[str, int]) -> bool:
        raise NotImplementedError()


class FixedCondition(Condition):

    def __init__(self, value: bool):
        self.value = value

    def eval(self, part: Dict[str, int]) -> bool:
        return self.value

    def is_always_false(self) -> bool:
        return self.value

    def __invert__(self):
        return FixedCondition(not self.value)

    def __and__(self, other: Condition):
        if self.value:
            return other
        else:
            return FixedCondition(False)

    def __or__(self, other: Condition):
        if self.value:
            return FixedCondition(True)
        else:
            return other


class IntervalCondition(Condition):

    def __init__(self, constraints: Dict[str, List[Tuple[int, int]]]):
        self.constraints = constraints

    def eval(self, part: Dict[str, int]) -> bool:
        valid = True
        for attrib, intervals in self.constraints.items():
            value = part[attrib]
            contained = False
            for interval in intervals:
                start, end = interval
                if (start is None or start <= value) and (end is None or value <= end):
                    contained = True
                    break
            if not contained:
                valid = False
                break
        return valid

    def is_always_false(self) -> bool:
        return False

    def __invert__(self):
        new_constraints = dict()
        for attrib, intervals in self.constraints.items():
            new_intervals = list()
            if intervals[0][0] is not None:
                new_intervals.append((None, intervals[0][0] - 1))
            for i in range(len(intervals) - 1):
                _, end = intervals[i]
                start_next, _ = intervals[i + 1]
                new_intervals.append((end + 1, start_next - 1))
            _, end = intervals[-1]
            if end is not None:
                new_intervals.append((end + 1, None))
            new_constraints[attrib] = new_intervals
        return IntervalCondition(new_constraints)

    def __and__(self, other: Condition) -> Condition:
        if isinstance(other, FixedCondition):
            return self if other.value else other
        new_constraints = dict()
        for attrib in set(self.constraints.keys()) | set(other.constraints.keys()):
            intervals1 = self.constraints.get(attrib)
            intervals2 = other.constraints.get(attrib)
            if intervals1 is None:
                new_constraints[attrib] = intervals2
            elif intervals2 is None:
                new_constraints[attrib] = intervals1
            else:
                new_constraints[attrib] = intersect_all(intervals1, intervals2)
                if len(new_constraints[attrib]) == 0:
                    return FixedCondition(False)
        return IntervalCondition(new_constraints)

    def __str__(self):
        return json.dumps(self.constraints)

    @classmethod
    def build(cls, attrib, uneq, value):
        if uneq == "<":
            interval = [None, value - 1]
        elif uneq == ">":
            interval = [value + 1, None]
        else:
            raise Exception(f"Invalid value {uneq}")
        return IntervalCondition({attrib: [interval]})


class Solver:

    def __init__(self):
        self.workflows = list()
        self.parts = list()

    def parse(self, file):
        with open(file) as hand:
            read_workflows = True
            for line in hand:
                line = line.strip()
                if read_workflows and line == "":
                    read_workflows = False
                    continue
                if read_workflows:
                    name, content = line[:-1].split("{", maxsplit=1)
                    rules_raw = content.split(",")
                    rules = list()
                    for raw in rules_raw[:-1]:
                        condition, target = raw.split(":", maxsplit=2)
                        attrib = condition[0]
                        uneq = condition[1]
                        value = int(condition[2:])
                        rules.append((attrib, uneq, value, target))
                    rules.append(rules_raw[-1])
                    self.workflows.append((name, rules))
                else:
                    attribs = line[1:-1].split(",", maxsplit=4)
                    part = dict()
                    for attrib in attribs:
                        key, value = attrib.split("=", maxsplit=1)
                        part[key] = int(value)
                    self.parts.append(part)

    def _get_acceptance_rules(self):
        to_workflow = dict()
        for workflow in self.workflows:
            name, rules = workflow
            rules_not_passed = FixedCondition(True)
            for rule in rules[:-1]:
                attrib, uneq, value, target_wf = rule
                if target_wf not in to_workflow:
                    to_workflow[target_wf] = list()
                rule = IntervalCondition.build(attrib, uneq, value)
                rules_to_pass = rules_not_passed & rule
                to_workflow[target_wf].append((name, rules_to_pass))
                rules_not_passed = rules_not_passed & ~rule
            target_wf = rules[-1]
            if target_wf not in to_workflow:
                to_workflow[target_wf] = list()
            to_workflow[target_wf].append((name, rules_not_passed))

        border = set()
        for wf, rule in to_workflow["A"]:
            border.add((wf, rule, ("A",)))

        final_rules = list()
        while len(border) > 0:
            current, rule_to_use, wf_used = border.pop()
            for wf, rule in to_workflow[current]:
                new_rule = rule & rule_to_use
                if new_rule.is_always_false():
                    continue

                used = [current]
                used.extend(wf_used)
                if wf == "in":
                    final_rules.append((tuple(used), new_rule))
                else:
                    border.add((wf, new_rule, tuple(used)))
        return final_rules

    def solve1(self):
        final_rules = self._get_acceptance_rules()

        result = 0
        for part in self.parts:
            for wfs_and_rule in final_rules:
                wfs, rule = wfs_and_rule
                if rule.eval(part):
                    for value in part.values():
                        result += value
                    break
        return result

    def solve2(self):
        final_rules = self._get_acceptance_rules()
        result = 0
        for wfs_and_rule in final_rules:
            wfs, rule = wfs_and_rule
            possibilities = 1
            for key in ["x", "m", "a", "s"]:
                intervals = rule.constraints.get(key)
                if intervals is None:
                    interval = [1, 4000]
                else:
                    interval = list(intervals[0])
                if interval[0] is None:
                    interval[0] = 1
                if interval[1] is None:
                    interval[1] = 4000
                possibilities *= (interval[1] - interval[0] + 1)
            result += possibilities
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
