from collections import Counter, defaultdict
from functools import lru_cache
from typing import Optional
from aoc2024.utils.reader import read_lines
from aoc2024.utils.timer import timer

lines = read_lines(is_test=False)


def stone_step(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    stone_str = str(stone)
    div, mod = divmod(len(stone_str), 2)
    if mod == 0:
        return [int(stone_str[:div]), int(stone_str[div:])]
    return [stone * 2024]


def dict_step(stones: dict[int, int]) -> dict[int, int]:
    new_dict: dict[int, int] = defaultdict(int)
    for stone, count in stones.items():
        for new_stone in stone_step(stone):
            new_dict[new_stone] += count
    return new_dict


def dict_steps(stones: dict[int, int], steps: int) -> int:
    for step in range(steps):
        stones = dict_step(stones)
    return sum(stones.values())


def part1():
    stones = [int(stone) for stone in lines[0].split(" ")]
    stone_map = dict(Counter(stones))
    return dict_steps(stone_map, 25)


def part2():
    stones = [int(stone) for stone in lines[0].split(" ")]
    stone_map = dict(Counter(stones))
    return dict_steps(stone_map, 75)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
