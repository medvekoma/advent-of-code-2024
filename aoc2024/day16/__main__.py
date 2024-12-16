from collections import Counter, defaultdict
from dataclasses import dataclass
from math import prod
from typing import Iterable

import numpy as np
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import group_list, parse_ints
from aoc2024.utils.mynumpy import Matrix, Pos2D
from aoc2024.utils.reader import read_lines

IS_TEST = False

lines = read_lines(IS_TEST)

type Reindeer = tuple[Pos2D, str]  # position, orientation (>, <, ^, v)


class Day:
    def __init__(self) -> None:
        self.matrix = Matrix.from_lines(lines)
        self.end = self.matrix.findall("E")[0]
        start = self.matrix.findall("S")[0]
        self.reindeer = (start, ">")

    def part1(self) -> None:
        pass


def parts():
    day = Day()
    day.part1()


parts()
