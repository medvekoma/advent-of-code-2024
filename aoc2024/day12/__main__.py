from typing import Optional
import numpy as np
import itertools
from collections import Counter, defaultdict
from functools import cache
from aoc2024.utils.mynumpy import Matrix
from aoc2024.utils.reader import read_lines

type Cell = tuple[int, int]

lines = read_lines(is_test=False)


class Day12:
    def __init__(self):
        self.matrix = Matrix.from_lines(lines)
        self.group_generator = itertools.count(start=1)
        self.cell_group_map: dict[Cell, int] = {}
        self.group_cell_map: dict[int, set[Cell]] = defaultdict(set)

    def next_group(self) -> int:
        return next(self.group_generator)

    def setup_group(self, cell: Cell) -> int:
        def mark_neighbors(cell: Cell):
            self.cell_group_map[cell] = group
            self.group_cell_map[group].add(cell)
            good_neighbors = [
                n
                for n in self.matrix.neighbors_of(cell)
                if self.matrix[n] == self.matrix[cell] and n not in self.cell_group_map
                #
            ]
            for neighbor in good_neighbors:
                mark_neighbors(neighbor)

        group = self.next_group()
        mark_neighbors(cell)
        return group

    def find_ungrouped_cell(self) -> Optional[Cell]:
        for cell in self.matrix.cells():
            if cell not in self.cell_group_map:
                return cell
        return None

    type Fence = tuple[int, int, bool]  # (x, y, is_horizontal; direction is always right or down)

    def fences(self, cell: Cell) -> list[Fence]:
        r, c = cell
        return [
            (r, c, True),
            (r, c, False),
            (r + 1, c, True),
            (r, c + 1, False),
        ]

    def bounding_fences(self, cells: set[Cell]) -> set[Fence]:
        all_fences = [fence for cell in cells for fence in self.fences(cell)]
        counter = Counter(all_fences)
        return {fence for fence, count in counter.items() if count == 1}

    def parts(self):
        while cell := self.find_ungrouped_cell():
            self.setup_group(cell)

        price1 = 0
        for cells in self.group_cell_map.values():
            fences = self.bounding_fences(cells)
            price1 += len(cells) * len(fences)
        print(f"part1: {price1}")
        # print(f"part2: {price2}")  # 886378 is too low; 1055706 is too high


def parts():
    Day12().parts()


parts()
