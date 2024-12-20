import numpy as np
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import group_list, parse_ints
from aoc2024.utils.mynumpy import Matrix, Pos2D
from aoc2024.utils.reader import read_lines
import networkx as nx

IS_TEST = False

lines = read_lines(IS_TEST)


class Day:
    def __init__(self) -> None:
        self.size = 7 if IS_TEST else 71
        self.limit = 12 if IS_TEST else 1024
        num_lines = [parse_ints(line) for line in lines]
        self.blocks = [Pos2D(x, y) for x, y in num_lines]
        self.graph = nx.Graph()

    def init_graph(self) -> None:
        forward_neighbors = [(0, 1), (1, 0)]
        for x in range(self.size):
            for y in range(self.size):
                if not ((x, y) in self.blocks):
                    for dx, dy in forward_neighbors:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size:
                            if not ((nx, ny) in self.blocks[: self.limit]):
                                self.graph.add_edge((x, y), (x + dx, y + dy))

    def draw_blocks(self) -> None:
        matrix = Matrix(np.full((self.size, self.size), "."))
        for x, y in self.blocks:
            matrix[x, y] = "#"
        print(matrix)

    def part1(self) -> None:
        # self.draw_blocks()
        self.init_graph()
        path_length = nx.dijkstra_path_length(self.graph, (0, 0), (self.size - 1, self.size - 1))
        print(f"Part 1: {path_length}")


if __name__ == "__main__":
    day = Day()
    day.part1()
