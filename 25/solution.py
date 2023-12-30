#!/usr/bin/env python
import collections
import random
from typing import Tuple


class EdgesStore:

    def __init__(self):
        self.lst = list()

    def add(self, source: str, target: str):
        self.lst.append([source, target])

    def get_random(self) -> Tuple[str, str]:
        return self.lst[random.randint(0, len(self.lst) - 1)]

    def __len__(self):
        return len(self.lst)

    def rename_nodes(self, node1: str, node2: str, new_name: str) -> None:
        for el in self.lst:
            for i in range(2):
                if el[i] == node1 or el[i] == node2:
                    el[i] = new_name
        self.lst = list(filter(
            lambda el: el[0] != el[1], self.lst
        ))


class Solver:

    def __init__(self):
        self.nodes = None
        self.edges = None

    def parse(self, file):
        self.nodes = dict()
        self.edges = set()
        with open(file) as hand:
            for line in hand:
                line = line.strip()
                source, targets = line.split(": ", maxsplit=2)
                targets = targets.split(" ")
                if source not in self.nodes:
                    self.nodes[source] = set()
                for target in targets:
                    if target not in self.nodes:
                        self.nodes[target] = set()
                    self.nodes[source].add(target)
                    self.nodes[target].add(source)
                    self.edges.add((source, target))

    def contract(self):
        # https://en.wikipedia.org/wiki/Karger%27s_algorithm
        edges = EdgesStore()
        nodes = set()
        for source, target in self.edges:
            edges.add(source, target)
            nodes.add(source)
            nodes.add(target)
        while len(nodes) > 2:
            source, target = edges.get_random()
            nodes.discard(source)
            nodes.discard(target)
            new_node = f"{source}-{target}"
            nodes.add(new_node)
            edges.rename_nodes(source, target, new_node)

        prod = 1
        for node in nodes:
            prod *= len(node.split("-"))

        return len(edges), prod

    def solve1(self):
        size, res = self.contract()
        while size > 3:
            size, res = self.contract()
        return res


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)


if __name__ == "__main__":
    main()
