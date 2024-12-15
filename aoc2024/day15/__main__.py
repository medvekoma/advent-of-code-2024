from collections import Counter, defaultdict
from math import prod
from typing import Iterable

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

    def move(self, pos: Pos2D, ori: str) -> Pos2D:
        cursor = pos
        buffer = []
        while True:
            char = self.matrix[cursor]
            if char == "#":
                break
            buffer.append(char)
            if char == ".":
                break
            cursor = cursor.add(self.offsets[ori])
        counter = Counter(buffer)
        if not counter.get("."):
            return pos
        buffer = [ch for ch in [".", "@", "O"] for _ in range(counter.get(ch, 0))]
        result = pos
        cursor = pos
        for ch in buffer:
            if ch == "@":
                result = cursor
            self.matrix[cursor] = ch
            cursor = cursor.add(self.offsets[ori])
        return result

    def price1(self) -> int:
        price = 0
        for r, c in self.matrix.cells():
            if self.matrix[r, c] == "O":
                price += 100 * r + c
        return price

    def part1(self) -> None:
        matches = np.where(self.matrix == "@")
        pos = Pos2D(matches[0][0], matches[1][0])
        for ori in self.sequence:
            pos = self.move(pos, ori)
        print(f"Part 1: {self.price1()}")


def parts():
    day = Day()
    day.part1()


parts()
