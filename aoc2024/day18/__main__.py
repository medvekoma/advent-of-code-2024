from typing import Optional
import networkx as nwx
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import parse_ints
from aoc2024.utils.mynumpy import Pos2D
from aoc2024.utils.reader import read_lines

IS_TEST = False

lines = read_lines(IS_TEST)


class Day:
    def __init__(self) -> None:
        self.size = 7 if IS_TEST else 71
        self.limit = 12 if IS_TEST else 1024
        num_lines = [parse_ints(line) for line in lines]
        self.blocks = [Pos2D(x, y) for x, y in num_lines]
        self.graph: nwx.Graph = nwx.Graph()

    def init_graph(self) -> None:
        first_blocks = self.blocks[: self.limit]
        forward_neighbors = [(0, 1), (1, 0)]
        cells = [(x, y) for x in range(self.size) for y in range(self.size)]
        for x, y in cells:
            if (x, y) in first_blocks:
                continue
            for dx, dy in forward_neighbors:
                nx, ny = x + dx, y + dy
                if nx >= self.size or ny >= self.size or (nx, ny) in first_blocks:
                    continue
                self.graph.add_edge((x, y), (nx, ny))

    @timer
    def part1(self) -> None:
        self.init_graph()
        path_length = self.get_path_length()
        print(f"Part 1: {path_length}")

    def get_path_length(self) -> Optional[int]:
        try:
            path_length = nwx.bidirectional_shortest_path(self.graph, (0, 0), (self.size - 1, self.size - 1))
            return len(path_length) - 1
        except nwx.NetworkXNoPath:
            return None

    @timer
    def part2(self) -> None:
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for x, y in self.blocks[self.limit :]:
            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                if self.graph.has_edge((x, y), (nx, ny)):
                    self.graph.remove_edge((x, y), (nx, ny))
            if not self.get_path_length():
                print(f"Part 2: {x},{y}")
                return


if __name__ == "__main__":
    day = Day()
    day.part1()
    day.part2()
