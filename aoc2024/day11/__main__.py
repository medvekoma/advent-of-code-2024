from collections import Counter
from functools import cache
from aoc2024.utils.reader import read_input

lines = read_input(is_test=False)
stone_list = [int(stone) for stone in lines[0].split(" ")]
stone_map = dict(Counter(stone_list))


@cache
def stone_step(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    stone_str = str(stone)
    div, mod = divmod(len(stone_str), 2)
    if mod == 0:
        return [int(stone_str[:div]), int(stone_str[div:])]
    return [stone * 2024]


def dict_step(stones: dict[int, int]) -> dict[int, int]:
    new_dict: dict[int, int] = {}  # defaultdict is somewhat slower
    for stone, count in stones.items():
        for new_stone in stone_step(stone):
            old_count = new_dict.get(new_stone, 0)
            new_dict[new_stone] = old_count + count
    return new_dict


def dict_steps(stones: dict[int, int], steps: int) -> int:
    for _ in range(steps):
        stones = dict_step(stones)
    return sum(stones.values())


def part1():
    return dict_steps(stone_map, 25)


def part2():
    return dict_steps(stone_map, 75)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
