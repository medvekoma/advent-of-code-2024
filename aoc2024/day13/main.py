from typing import Iterable
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import parse_ints, split_by
from aoc2024.utils.reader import read_input

lines = read_input(is_test=False)

type Cell = list[int]  # always contains two elements: x and y
type Group = list[Cell]  # always contains three elements: A, B and W (winning target)


class Day13:
    def __init__(self) -> None:
        self.groups: list[Group] = [
            [parse_ints(line) for line in block]
            for block in split_by(lines, "")
            #
        ]

    def solve_group(self, group: Group) -> Iterable[Cell]:
        (ax, ay), (bx, by), (wx, wy) = group
        divident = wy * ax - wx * ay
        divisor = by * ax - bx * ay
        if divisor == 0:
            if divident == 0:
                # possibly more solutions
                steps, mod = divmod(wx, ax)
                if mod == 0:
                    yield [steps, 0]
                steps, mod = divmod(wx, bx)
                if mod == 0:
                    yield [0, steps]
        else:
            b, mod = divmod(divident, divisor)
            if mod == 0:
                a, mod = divmod(wx - b * bx, ax)
                if mod == 0:
                    yield [a, b]

    def price(self, cell: Cell) -> int:
        return 3 * cell[0] + 1 * cell[1]

    def part1(self):
        price = 0
        for group in self.groups:
            solutions = [(a, b) for a, b in self.solve_group(group) if a <= 100 and b <= 100]
            if solutions:
                price += min(self.price(cell) for cell in solutions)
        print(f"part1: {price}")

    def part2(self):
        new_groups = [
            (a, b, (wx + 10000000000000, wy + 10000000000000))
            for a, b, (wx, wy) in self.groups
            #
        ]
        price = 0
        for group in new_groups:
            solutions = list(self.solve_group(group))
            if solutions:
                price += min(self.price(cell) for cell in solutions)
        print(f"part2: {price}")


@timer
def parts():
    day13 = Day13()
    day13.part1()
    day13.part2()


parts()
