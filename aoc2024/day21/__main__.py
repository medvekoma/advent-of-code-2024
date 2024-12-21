from collections import defaultdict
from math import prod
from typing import Iterable

import numpy as np
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import group_list, parse_ints
from aoc2024.utils.reader import read_lines

IS_TEST = True

lines = read_lines(IS_TEST)


class Day:
    def __init__(self) -> None:
        self.lines = lines

    def part1(self) -> None:
        print(self.lines)


def main():
    day = Day()
    day.part1()


if __name__ == "__main__":
    main()
