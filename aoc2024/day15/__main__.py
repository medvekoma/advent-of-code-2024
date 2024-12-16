from collections import Counter, defaultdict
from math import prod
from typing import Iterable, Optional

import numpy as np
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import group_list, parse_ints, split_by
from aoc2024.utils.mynumpy import Matrix, Pos2D
from aoc2024.utils.reader import read_lines

IS_TEST = False

lines = read_lines(IS_TEST)


class Day:
    def __init__(self) -> None:
        blocks = list(split_by(lines, ""))
        self.matrix = Matrix.from_lines(blocks[0])
        self.sequence = "".join(blocks[1])
        self.offsets = {
            "^": (-1, 0),
            "v": (1, 0),
            ">": (0, 1),
            "<": (0, -1),
        }

    def price1(self) -> int:
        price = 0
        for r, c in self.matrix.cells():
            if self.matrix[r, c] == "O":
                price += 100 * r + c
        return price

    def moverec(self, pos: Pos2D, ori: str) -> Optional[Pos2D]:
        nextpos = pos.add(self.offsets[ori])
        nextchar = self.matrix[nextpos]
        if nextchar == "#":
            return None
        if nextchar == "." or self.moverec(nextpos, ori):
            self.matrix[nextpos] = self.matrix[pos]
            self.matrix[pos] = "."
            return nextpos
        return None

    def part1(self) -> None:
        pos = self.matrix.findall("@")[0]
        for ori in self.sequence:
            pos = self.moverec(pos, ori) or pos
        print(f"Part 1: {self.price1()}")


def parts():
    Day().part1()


parts()
