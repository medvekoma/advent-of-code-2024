import re
from typing import Optional
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
            print(res)

    def solve_group(self, group: Group) -> Optional[Cell]:
        print(group)
        (ax, ay), (bx, by), (wx, wy) = group
        divident = wy * ax - wx * ay
        divisor = by * ax - bx * ay
        if divisor == 0:
            if divident == 0:
                asteps, amod = divmod(wx, ax)
                bsteps, bmod = divmod(wx, bx)
                if amod != 0 and bmod != 0:
                    return None
                if amod == 0 and bmod == 0:
                    aprice = asteps * 3
                    bprice = bsteps * 1
                    if aprice <= bprice:
                        return (asteps, 0)
                    else:
                        return (0, bsteps)
                if amod == 0:
                    return (asteps, 0)
                return (0, bsteps)
            return None
        b, bmod = divmod(divident, divisor)
        if bmod != 0:
            return None
        a, amod = divmod(wx - b * bx, ax)
        if amod != 0:
            return None
        return a, b


Day13()
