from aoc2024.utils.collections import parse_lines
from aoc2024.utils.reader import read_lines


lines = read_lines(is_test=True)
groups = parse_lines(lines, r"(\d+)\s+\-\s+(\d+)\s+\-\s+(\w+)")


def part1():
    return groups


def part2():
    return -1


print(f"part1: {part1()}")
print(f"part2: {part2()}")
