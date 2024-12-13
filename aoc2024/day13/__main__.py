import re
from typing import Iterable, Optional
from aoc2024.utils.collections import split_by
from aoc2024.utils.reader import read_lines

lines = read_lines(is_test=True)

type Cell = tuple[int, int]
type Group = tuple[Cell, Cell, Cell]


class Day13:
    def __init__(self) -> None:
        self.groups: list[Group] = [
            tuple(map(int, re.findall(r"\d+", line)) for line in block)
            for block in split_by(lines, "")
            #
        ]
        for group in self.groups:
            res = self.solve_group(group)
            print(list(res))

    def solve_group(self, group: Group) -> Iterable[Cell]:
        print(group)
        (ax, ay), (bx, by), (wx, wy) = group
        divident = wy * ax - wx * ay
        divisor = by * ax - bx * ay
        if divisor == 0:
            if divident == 0:
                # possible more solutions
                asteps, amod = divmod(wx, ax)
                if amod == 0:
                    yield (asteps, 0)
                bsteps, bmod = divmod(wx, bx)
                if bmod == 0:
                    yield (0, bsteps)
        else:
            b, bmod = divmod(divident, divisor)
            if bmod == 0:
                a, amod = divmod(wx - b * bx, ax)
                if amod == 0:
                    yield a, b


Day13()
