from collections import Counter, defaultdict
from functools import lru_cache
from typing import Optional
from aoc2024.utils.reader import read_lines
from aoc2024.utils.timer import timer

lines = read_lines(is_test=False)


@lru_cache
def stone_step_str(stone: str) -> tuple[str, Optional[str]]:
    if stone == "0":
        return ("1", None)
    div, mod = divmod(len(stone), 2)
    if mod == 0:
        return (stone[:div], stone[div:].lstrip("0") or "0")
    return (str(int(stone) * 2024), None)


@lru_cache(maxsize=1000000)
def stone_step(stone: int) -> tuple[int, Optional[int]]:
    if stone == 0:
        return (1, None)
    stone_str = str(stone)
    div, mod = divmod(len(stone_str), 2)
    if mod == 0:
        return (int(stone_str[:div]), int(stone_str[div:]))
    return (stone * 2024, None)


def list_step(stones: list[int]) -> list[int]:
    new_stones = []
    for i, stone in enumerate(stones):
        a, b = stone_step(stone)
        stones[i] = a
        if b is not None:
            new_stones.append(b)
    return stones + new_stones


def list_steps(stones: list[int], steps: int) -> int:
    for step in range(steps):
        stones = list_step(stones)
    return len(stones)


@timer
def part1():
    stones = [int(stone) for stone in lines[0].split(" ")]
    return list_steps(stones, 25)


def dict_step(stones: dict[int, int]) -> dict[int, int]:
    new_dict: dict[int, int] = defaultdict(int)
    for stone, count in stones.items():
        stone1, stone2 = stone_step(stone)
        new_dict[stone1] += count
        if stone2 is not None:
            new_dict[stone2] += count
    return new_dict


def dict_steps(stones: dict[int, int], steps: int) -> int:
    for step in range(steps):
        stones = dict_step(stones)
    return sum(stones.values())


@timer
def part2():
    stones = [int(stone) for stone in lines[0].split(" ")]
    stone_map = dict(Counter(stones))
    return dict_steps(stone_map, 75)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
