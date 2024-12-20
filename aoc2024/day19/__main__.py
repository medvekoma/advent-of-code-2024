from functools import lru_cache

from aoc2024.utils.collections import split_by
from aoc2024.utils.reader import read_lines

IS_TEST = False

lines = read_lines(IS_TEST)


class Day19:
    def __init__(self) -> None:
        towels, self.patterns = split_by(lines, "")
        self.towels = towels[0].split(", ")

    def is_possible(self, pattern: str) -> bool:
        if not pattern:
            return True
        possible_towels = [
            towel
            for towel in self.towels
            if pattern.startswith(towel)
            #
        ]
        for towel in sorted(possible_towels, key=len, reverse=True):
            if self.is_possible(pattern[len(towel) :]):
                return True
        return False

    def part1(self) -> None:
        result = 0
        for pattern in self.patterns:
            if self.is_possible(pattern):
                result += 1
        print(f"Part 1: {result}")

    @lru_cache
    def count_all(self, pattern: str) -> int:
        if not pattern:
            return 1
        return sum(
            self.count_all(pattern[len(towel) :])
            for towel in self.towels
            if pattern.startswith(towel)
            #
        )

    def part2(self) -> None:
        result = 0
        for pattern in self.patterns:
            result += self.count_all(pattern)
        print(f"Part 2: {result}")


def parts():
    day = Day19()
    day.part1()
    day.part2()


parts()
