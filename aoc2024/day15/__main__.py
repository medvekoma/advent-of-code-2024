from typing import Optional

from aoc2024.utils.collections import split_by
from aoc2024.utils.mynumpy import Matrix, Pos2D
from aoc2024.utils.reader import read_lines

IS_TEST = False

lines = read_lines(IS_TEST)


class Day:
    def __init__(self) -> None:
        blocks = list(split_by(lines, ""))
        self.matrix_lines = blocks[0]
        self.matrix = Matrix.from_lines(self.matrix_lines)

        self.sequence = "".join(blocks[1])
        self.offsets = {
            "^": (-1, 0),
            "v": (1, 0),
            ">": (0, 1),
            "<": (0, -1),
        }

    def price(self) -> int:
        price = 0
        for r, c in self.matrix.cells():
            if self.matrix[r, c] in ["O", "["]:
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
        print(f"Part 1: {self.price()}")

    def extend_positions(self, positions: set[Pos2D]) -> set[Pos2D]:
        result = positions.copy()
        for pos in positions:
            if self.matrix[pos] == "]":
                result.add(pos.add((0, -1)))
            if self.matrix[pos] == "[":
                result.add(pos.add((0, 1)))
        return result

    def move_vert(self, positions: set[Pos2D], ori: str) -> Optional[Pos2D]:
        next_positions = {pos.add(self.offsets[ori]) for pos in positions}
        next_chars = {self.matrix[pos] for pos in next_positions}
        if "#" in next_chars:
            return None
        if next_chars != {"."}:
            next_positions = {pos for pos in next_positions if self.matrix[pos] != "."}
            next_positions = self.extend_positions(next_positions)
            if not self.move_vert(next_positions, ori):
                return None
        for pos in positions:
            next_pos = pos.add(self.offsets[ori])
            self.matrix[next_pos] = self.matrix[pos]
            self.matrix[pos] = "."
        return next_pos

    def part2(self) -> None:
        double_lines = [
            line.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.")
            for line in self.matrix_lines
            #
        ]
        self.matrix = Matrix.from_lines(double_lines)
        pos = self.matrix.findall("@")[0]
        for ori in self.sequence:
            if ori in ["v", "^"]:
                pos = self.move_vert({pos}, ori) or pos
            else:
                pos = self.moverec(pos, ori) or pos
        price = self.price()
        print(f"Part 2: {price}")  # 1536090 is too low


def parts():
    Day().part1()
    Day().part2()


parts()
