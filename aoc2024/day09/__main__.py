from collections import deque
from dataclasses import dataclass
from typing import Optional
from aoc2024.utils.reader import read_lines

lines = read_lines(is_test=False)


def process_line(line: str) -> list[int]:
    result = []
    for i, ch in enumerate(line):
        length = int(ch)
        is_file = i % 2 == 0
        if is_file:
            fid = i // 2
            result += [fid] * length
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
    for idx, fid in enumerate(disk):
        if fid == -1:
            break
        result += fid * idx
    return result


def part1():
    disk = process_line(lines[0])
    disk = defragment1(disk)
    checksum = check_sum(disk)
    return checksum


print(f"part1: {part1()}")


@dataclass
class Block:
    start: int
    length: int


@dataclass
class File:
    fid: int
    block: Block


class Part2:
    def __init__(self, line: str) -> None:
        self.free_blocks: deque[Block] = deque([])
        self.files: deque[File] = deque([])
        cursor = 0
        for i, ch in enumerate(line):
            length = int(ch)
            if length == 0:
                continue
            block = Block(cursor, length)
            is_file = i % 2 == 0
            if is_file:
                fid = i // 2
                self.files.appendleft(File(fid, block))
            else:
                self.free_blocks.append(block)
            cursor += length

    def defragment_file(self, file: File) -> None:
        for free_block in self.free_blocks:
            if free_block.start > file.block.start:
                return
            if free_block.length >= file.block.length:
                new_file_start = free_block.start
                remaining_space = free_block.length - file.block.length
                free_block.start += file.block.length
                free_block.length = remaining_space
                file.block.start = new_file_start
                return

    def defragment_files(self) -> None:
        for file in self.files:
            self.defragment_file(file)

    def file_checksum(self, file: File) -> int:
        result = 0
        for i in range(file.block.length):
            result += file.fid * (file.block.start + i)
        return result

    def run(self) -> int:
        self.defragment_files()
        result = sum(self.file_checksum(file) for file in self.files)
        return result


def part2():
    return Part2(lines[0]).run()


print(f"part2: {part2()}")
