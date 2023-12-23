#!/usr/bin/env python

import collections
import math


class ModulesEvaluator:

    def __init__(self, modules, module_to_inputs):
        self.modules = modules
        self.module_to_inputs = module_to_inputs
        self.monitored_modules = set()

    def get_initial_status(self):
        status = dict()
        for mod, type_and_targets in self.modules.items():
            mod_type, targets = type_and_targets
            if mod_type == "broadcaster":
                mod_status = None
            elif mod_type == "%":
                mod_status = False
            else:
                mod_inputs = self.module_to_inputs[mod]
                mod_status = {mod_input: False for mod_input in mod_inputs}
            status[mod] = mod_status
        return status

    def eval(self, status):
        if status is None:
            status = self.get_initial_status()
        activations = collections.deque()
        activations.append(("broadcaster", False, "button"))
        n_high_sent, n_low_sent = 0, 0
        monitored = {el: False for el in self.monitored_modules}
        while len(activations) > 0:
            mod, high_pulse, source = activations.popleft()
            # Increase counts
            if high_pulse:
                n_high_sent += 1
            else:
                n_low_sent += 1
            if mod in monitored and not high_pulse:
                monitored[mod] = True
            # Process
            if mod not in self.modules:
                continue
            mod_type, targets = self.modules[mod]
            if mod_type == "broadcaster":
                for target in targets:
                    activations.append((target, high_pulse, mod))
            elif mod_type == "%":
                if not high_pulse:
                    status[mod] = not status[mod]
                    for target in targets:
                        activations.append((target, status[mod], mod))
            else:
                status[mod][source] = high_pulse
                all_high = True
                for pulse in status[mod].values():
                    if not pulse:
                        all_high = False
                        break
                for target in targets:
                    activations.append((target, not all_high, mod))
        return (n_high_sent, n_low_sent), status, monitored

    def get_ancestors_evaluator(self, node):
        ancestors = set()
        current = {node}
        while len(current) > 0:
            node = current.pop()
            if node in self.module_to_inputs:
                for parent in self.module_to_inputs[node]:
                    if parent not in ancestors:
                        current.add(parent)
            ancestors.add(node)
        sub_modules = dict()
        for el, item in self.modules.items():
            if el in ancestors:
                sub_modules[el] = item
        sub_mod_to_inputs = dict()
        for el, inputs in self.module_to_inputs.items():
            sub_mod_to_inputs[el] = inputs
        return ModulesEvaluator(modules=sub_modules, module_to_inputs=sub_mod_to_inputs)

    @classmethod
    def build(cls, modules_list):
        modules = dict()
        module_to_inputs = dict()
        for mod_with_targets in modules_list:
            mod, targets = mod_with_targets
            if mod == "broadcaster":
                mod_name = mod
                mod_type = mod
            else:
                mod_type = mod[0]
                mod_name = mod[1:]
            modules[mod_name] = (mod_type, targets)
            for target in targets:
                if target not in module_to_inputs:
                    module_to_inputs[target] = list()
                module_to_inputs[target].append(mod_name)
        return ModulesEvaluator(modules, module_to_inputs)


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, file):
        self.data = list()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                mod, targets = line.split(" -> ", maxsplit=2)
                targets = targets.split(", ")
                self.data.append((mod, targets))

    def _press_btn(self, times: int) -> int:
        evaluator = ModulesEvaluator.build(self.data)
        status = None
        pulses_high = 0
        pulses_low = 0
        pulses_by_step = list()
        for i in range(times):
            pulses_by_step.append((pulses_high, pulses_low))
            pulses_sent, status, _ = evaluator.eval(status)
            sent_high, sent_low = pulses_sent
            pulses_high += sent_high
            pulses_low += sent_low
        return pulses_high * pulses_low

    def get_period(self, root_evaluator: ModulesEvaluator, node: str):
        evaluator = root_evaluator.get_ancestors_evaluator(node)
        evaluator.monitored_modules.add(node)
        status = None
        presses = 0

        while True:
            _, status, monitored = evaluator.eval(status)
            presses += 1
            if monitored[node]:
                break
        return presses

    def solve1(self):
        return self._press_btn(1000)

    def solve2(self):
        evaluator = ModulesEvaluator.build(self.data)

        dd_node = evaluator.module_to_inputs["rx"][0]
        periods = list()
        for node in evaluator.module_to_inputs[dd_node]:
            period = self.get_period(evaluator, node)
            periods.append(period)

        return math.lcm(*periods)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
