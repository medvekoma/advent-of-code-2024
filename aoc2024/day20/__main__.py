from collections import Counter, defaultdict
from itertools import combinations
from math import prod
from multiprocessing import Pool
from typing import Iterable, Optional

import numpy as np
import networkx as nwx
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import group_list, parse_ints
from aoc2024.utils.mynumpy import Matrix, Pos2D
from aoc2024.utils.reader import read_lines

type BlockSourceTarget = tuple[Pos2D, Pos2D, Pos2D]


IS_TEST = False

lines = read_lines(IS_TEST)


class Day:
    def __init__(self) -> None:
        self.treshold = 1 if IS_TEST else 100
        self.matrix = Matrix.from_lines(lines)
        self.start = self.matrix.findall("S")[0]
        self.end = self.matrix.findall("E")[0]
        self.matrix[self.start] = "."
        self.matrix[self.end] = "."
        self.graph: nwx.Graph = nwx.Graph()
        self.blocks: set[Pos2D] = set()
        self.initialize_graph()

    def initialize_graph(self) -> None:
        neighbors = [(0, 1), (1, 0)]
        for pos in self.matrix.cells():
            if self.matrix[pos] != ".":
                self.blocks.add(pos)
                continue
            for dpos in neighbors:
                npos = pos.add(dpos)
                if self.matrix.get_value(npos) == ".":
                    self.graph.add_edge(pos, npos)

    def collect_shortcuts(self) -> set[BlockSourceTarget]:
        result: list[BlockSourceTarget] = []
        for pos in self.blocks:
            empty_neighbors = {
                neighbor
                for neighbor in self.matrix.neighbors_of(pos)
                if self.matrix[neighbor] == "."
                #
            }
            if len(empty_neighbors) in [2, 3]:
                for n1, n2 in combinations(empty_neighbors, 2):
                    result.append((pos, n1, n2))
        return result

    def potential_block(self, bst: BlockSourceTarget) -> Optional[Pos2D]:
        block, source, target = bst
        try:
            path_length = nwx.shortest_path_length(self.graph, source, target)
            return block if path_length > self.treshold + 1 else None
        except nwx.NetworkXNoPath:
            return None

    def filter_long_paths_parallel(self, lbst: list[BlockSourceTarget]) -> set[Pos2D]:
        blocks = {self.potential_block(bst) for bst in lbst}
        # with Pool(processes=8) as pool:
        #     blocks = pool.map(self.potential_block, (bst for bst in lbst))
        return {block for block in blocks if block is not None}

    def part1(self) -> None:
        length = nwx.shortest_path_length(self.graph, self.start, self.end)
        print(f"length: {length}")
        shortcuts = self.collect_shortcuts()
        print(len(shortcuts))
        filtered = self.filter_long_paths_parallel(shortcuts)
        edges = []
        results = []
        for block in filtered:
            free_neighbors = [n for n in self.matrix.neighbors_of(block) if self.matrix[n] == "."]
            for b1, b2 in edges:
                if self.graph.has_edge(b1, b2):
                    self.graph.remove_edge(b1, b2)
            for nb in free_neighbors:
                self.graph.add_edge(nb, block)
            edges = [(block, nb) for nb in free_neighbors]
            new_length = nwx.shortest_path_length(self.graph, self.start, self.end)
            if length - new_length >= self.treshold:
                results.append(length - new_length)
            # print(f"new_length: {new_length}, diff: {length - new_length}")
        print(f"Part 1: {len(results)}")
        # result = len(path_length) - 1
        # print(f"Part 1: {result}")


if __name__ == "__main__":
    day = Day()
    day.part1()
