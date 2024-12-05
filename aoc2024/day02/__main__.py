from aoc2024.utils.collections import remove_at
from aoc2024.utils.reader import read_lines


lines = read_lines()
numbers = [[int(level) for level in line.split()] for line in lines]
good_sets = [{1, 2, 3}, {-1, -2, -3}]


def is_safe(levels: list[int]) -> bool:
    diffs = {x - y for x, y in zip(levels, levels[1:])}
    return any(diffs.issubset(good_set) for good_set in good_sets)


def part1():
    safe_levels = [is_safe(level) for level in numbers]
    return safe_levels.count(True)


def part2():
    def first_bad(levels: list[int]) -> int:
        diffs = [x - y for x, y in zip(levels, levels[1:])]
        if diffs[0] in good_sets[0]:
            good_set = good_sets[0]
        elif diffs[0] in good_sets[1]:
            good_set = good_sets[1]
        else:
            return 0
        for i, diff in enumerate(diffs[1:]):
            if diff not in good_set:
                return i + 1
        return -1

    def is_safe2(levels: list[int]) -> bool:
        if is_safe(levels):
            return True
        bad_index = first_bad(levels)
        if bad_index == 1:
            levels0 = remove_at(levels, 0)
            if is_safe(levels0):
                return True
        levels1 = remove_at(levels, bad_index)
        if is_safe(levels1):
            return True
        levels2 = remove_at(levels, bad_index + 1)
        return is_safe(levels2)

    safe_levels = [is_safe2(level) for level in numbers]
    return safe_levels.count(True)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
