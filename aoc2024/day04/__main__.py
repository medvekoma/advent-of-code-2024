from aoc2024.utils.collections import parse_lines
from aoc2024.utils.reader import read_lines


lines = read_lines(is_test=True)


def part1():
    matches = parse_lines(lines, r"(\d+),\s*(\w+)")
    return matches


def part2():
    pass


print(f"part1: {part1()}")
print(f"part2: {part2()}")
