from typing import Optional
from aoc2024.utils.reader import read_lines

lines = read_lines(is_test=True)


def process_line(line: str) -> list[int]:
    result = []
    for i, ch in enumerate(line):
        length = int(ch)
        is_file = i % 2 == 0
        if is_file:
            id = i // 2
            result += [id] * length
        else:
            result += [-1] * length
    return result


def next_free_idx(disk: list[int], idx: int) -> Optional[int]:
    while True:
        idx += 1
        if idx >= len(disk):
            return None
        if disk[idx] == -1:
            return idx


def prev_used_idx(disk: list[int], idx: int) -> Optional[int]:
    while True:
        idx -= 1
        if idx < 0:
            return None
        if disk[idx] != -1:
            return idx


def defragment1(disk: list[int]) -> list[int]:
    free_idx = next_free_idx(disk, 0)
    used_idx = prev_used_idx(disk, len(disk))
    while free_idx and used_idx and free_idx < used_idx:
        disk[free_idx] = disk[used_idx]
        disk[used_idx] = -1
        free_idx = next_free_idx(disk, free_idx)
        used_idx = prev_used_idx(disk, used_idx)
    return disk


def check_sum(disk: list[int]) -> int:
    result = 0
    for idx, id in enumerate(disk):
        if id == -1:
            break
        result += id * idx
    return result


def part1():
    disk = process_line(lines[0])
    disk = defragment1(disk)
    checksum = check_sum(disk)
    return checksum


print(f"part1: {part1()}")
