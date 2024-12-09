from typing import Optional
from aoc2024.utils.timer import timer
from aoc2024.utils.collections import remove_at
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

type Block = tuple[int, int]  # (start, length)
type File = tuple[int, Block]  # (id, block)]


class Part2:
    def __init__(self) -> None:
        self.free_blocks: list[Block] = []
        self.unmoved_files: list[File] = []
        self.moved_files: list[File] = []

    def process_line(self, line: str) -> None:
        cursor = 0
        for i, ch in enumerate(line):
            length = int(ch)
            if length == 0:
                continue
            block = (cursor, length)
            cursor += length
            is_file = i % 2 == 0
            if is_file:
                fid = i // 2
                self.unmoved_files.insert(0, (fid, block))
            else:
                self.free_blocks.append(block)

    def defragment_step(self) -> bool:
        for free_idx, free_block in enumerate(self.free_blocks):
            for file_idx, file in enumerate(self.unmoved_files):
                fid, file_block = file
                if file_block[0] < free_block[0]:
                    continue
                if free_block[1] >= file_block[1]:
                    file = (fid, (free_block[0], file_block[1]))
                    remaining_space = free_block[1] - file_block[1]
                    if remaining_space == 0:
                        self.free_blocks = remove_at(self.free_blocks, free_idx)
                    else:
                        self.free_blocks[free_idx] = (free_block[0] + file_block[1], remaining_space)
                    self.unmoved_files = remove_at(self.unmoved_files, file_idx)
                    self.moved_files.append(file)
                    return True
        return False

    def dump(self):
        print(f"free_blocks: {self.free_blocks}")
        print(f"unmoved_files: {self.unmoved_files}")
        print(f"moved_files: {self.moved_files}")

    def file_checksum(self, file: File) -> int:
        result = 0
        fid, (start, length) = file
        for i in range(length):
            result += fid * (start + i)
        return result

    @timer
    def run(self, line: str) -> int:
        self.process_line(line)
        # self.dump()
        while self.defragment_step():
            pass
        moved_checksum = sum([self.file_checksum(file) for file in self.moved_files])
        unmoved_checksum = sum([self.file_checksum(file) for file in self.unmoved_files])
        return moved_checksum + unmoved_checksum


part2 = Part2().run(lines[0])
print(f"part2: {part2}")
