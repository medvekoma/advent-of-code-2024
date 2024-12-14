from typing import Optional
import itertools
from collections import defaultdict
from aoc2024.utils.benchmark import timer
from aoc2024.utils.mynumpy import Matrix
from aoc2024.utils.reader import read_lines

type Cell = tuple[int, int]

lines = read_lines(is_test=False)


class Day12:
    def __init__(self) -> None:
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

    type Fence = tuple[tuple[int, int], tuple[int, int]]  # Directed segments, clockwise

    def fences(self, cell: Cell) -> list[Fence]:
        r, c = cell
        return [
            ((r + 0, c + 0), (r + 0, c + 1)),
            ((r + 0, c + 1), (r + 1, c + 1)),
            ((r + 1, c + 1), (r + 1, c + 0)),
            ((r + 1, c + 0), (r + 0, c + 0)),
        ]

    def segmenter(self, fence: Fence):
        return tuple(sorted(fence))

    def bounding_fences(self, cells: set[Cell]) -> set[Fence]:
        all_fences = [fence for cell in cells for fence in self.fences(cell)]
        fence_dict = defaultdict(list)
        for fence in all_fences:
            fence_dict[self.segmenter(fence)].append(fence)
        return {fences[0] for fences in fence_dict.values() if len(fences) == 1}

    def direction(self, fence: Fence) -> tuple[int, int]:
        (r1, c1), (r2, c2) = fence
        return (r2 - r1, c2 - c1)

    def get_sides(self, fences: set[Fence]) -> int:
        direction_groups = itertools.groupby(sorted(fences, key=self.direction), key=self.direction)
        sides = 0
        for direction, dir_fences in direction_groups:
            dir_idx = 0 if direction[0] == 0 else 1
            cells = [fence[0] for fence in dir_fences]
            # pylint: disable=cell-var-from-loop
            for _, cell_group in itertools.groupby(sorted(cells, key=lambda c: c[dir_idx]), key=lambda c: c[dir_idx]):
                indices = [cell[1 - dir_idx] for cell in cell_group]
                diffs = {v - i for i, v in enumerate(sorted(indices))}
                sides += len(diffs)
        return sides

    def parts(self):
        while cell := self.find_ungrouped_cell():
            self.setup_group(cell)

        price1 = 0
        price2 = 0
        for cells in self.group_cell_map.values():
            fences = self.bounding_fences(cells)
            price1 += len(cells) * len(fences)
            sides = self.get_sides(fences)
            price2 += len(cells) * sides
        print(f"part1: {price1}")
        print(f"part2: {price2}")  # 886378 is too low; 1055706 is too high -- 897702


@timer
def parts():
    day12 = Day12()
    day12.parts()


parts()
