from collections import Counter, defaultdict, deque
from math import prod
from typing import Iterable, Optional

import numpy as np
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import group_list, parse_ints, split_by, split_by_func
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

    def extend_chunk(self, chunk: list[Pos2D]) -> list[Pos2D]:
        if self.matrix[chunk[0]] == "]":
            chunk = [chunk[0].add((0, -1))] + chunk
        if self.matrix[chunk[-1]] == "[":
            chunk = chunk + [chunk[-1].add((0, 1))]
        return chunk

    def get_steps_vert(self, positions: list[Pos2D], ori: str, prev_steps: int = 0) -> int:
        next_positions = [pos.add(self.offsets[ori]) for pos in positions]
        next_chars = [self.matrix[pos] for pos in next_positions]
        if "#" in next_chars:
            return 0
        if set(next_chars) == {"."}:
            return prev_steps + 1
        next_chunks = list(split_by_func(next_positions, lambda pos: self.matrix[pos] == "."))
        next_chunks = [self.extend_chunk(chunk) for chunk in next_chunks]
        return min(
            self.get_steps_vert(chunk, ori, prev_steps + 1)
            for chunk in next_chunks
            #
        )

    def part1(self) -> None:
        pos = self.matrix.findall("@")[0]
        for ori in self.sequence:
            pos = self.moverec(pos, ori) or pos
        print(f"Part 1: {self.price1()}")


def parts():
    Day().part1()


parts()
