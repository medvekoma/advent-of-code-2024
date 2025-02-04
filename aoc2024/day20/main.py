from itertools import combinations
from typing import Optional

import networkx as nwx
from aoc2024.utils.benchmark import timer
from aoc2024.utils.mynumpy import Matrix, Pos2D
from aoc2024.utils.reader import read_input

type Cell = tuple[int, int]
type BlockSourceTarget = tuple[Cell, Cell, Cell]


IS_TEST = False

lines = read_input(IS_TEST)


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

    def collect_shortcuts(self) -> list[BlockSourceTarget]:
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

    def potential_block(self, bst: BlockSourceTarget) -> Optional[Cell]:
        block, source, target = bst
        try:
            path_length = nwx.shortest_path_length(self.graph, source, target)
            return block if path_length > self.treshold + 1 else None
        except nwx.NetworkXNoPath:
            return None

    def filter_long_paths_parallel(self, lbst: list[BlockSourceTarget]) -> set[Cell]:
        blocks = {self.potential_block(bst) for bst in lbst}
        return {block for block in blocks if block is not None}

    @timer
    def part1(self) -> None:
        length = nwx.shortest_path_length(self.graph, self.start, self.end)
        shortcuts = self.collect_shortcuts()
        filtered = self.filter_long_paths_parallel(shortcuts)
        edges: list[tuple[Cell, Cell]] = []
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
        print(f"Part 1: {len(results)}")

    @timer
    def part2(self) -> None:
        def get_shortcut_length(pos1: Pos2D, pos2: Pos2D) -> int:
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        path = nwx.shortest_path(self.graph, self.start, self.end)
        result = 0
        for i1 in range(len(path) - self.treshold):
            for i2 in range(i1 + 1 + self.treshold, len(path)):
                pos1 = path[i1]
                pos2 = path[i2]
                shortcut_length = get_shortcut_length(pos1, pos2)
                winning = i2 - i1 - shortcut_length
                if shortcut_length <= 20 and winning >= self.treshold:
                    result += 1
        print(f"Part 2: {result}")


def main():
    day = Day()
    day.part1()
    day.part2()


if __name__ == "__main__":
    main()
