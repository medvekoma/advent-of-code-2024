from dataclasses import dataclass
from itertools import groupby
from typing import Iterator, Optional
from aoc2024.utils.timer import timer
from aoc2024.utils.reader import read_lines

lines = read_lines(is_test=True)


@dataclass
class Block:
    start: int
    length: int


@dataclass
class File:
    id: int
    block: Block


class Day09:

    def __init__(self, line: str):
        self.blocks: list[int] = []
        for i, ch in enumerate(line):
            length = int(ch)
            is_file = i % 2 == 0
            if is_file:
                fid = i // 2
                self.blocks += [fid] * length
            else:
                self.blocks += [-1] * length
        self.moved_ids: set[int] = set()

    def free_blocks(self) -> Iterator[Block]:
        groupings = groupby(enumerate(self.blocks), key=lambda x: x[1])
        for fid, group in groupings:
            if fid == -1:
                blocks = list(group)
                yield Block(blocks[0][0], len(blocks))

    def files(self) -> Iterator[File]:
        reversed_blocks = reversed(self.blocks)
        groupings = groupby(enumerate(reversed_blocks), key=lambda x: x[1])
        for fid, group in groupings:
            if fid != -1:
                blocks = list(group)
                yield File(fid, Block(len(self.blocks) - blocks[-1][0] - 1, len(blocks)))

    def defragment_step(self) -> bool:
        for file in self.files():
            # print(f"file: {file}")
            for free_block in self.free_blocks():
                # print(f"  free_block: {free_block}")
                if file.id in self.moved_ids:
                    continue
                if file.block.start < free_block.start:
                    continue
                if free_block.length >= file.block.length:
                    for i in range(file.block.length):
                        self.blocks[free_block.start + i] = file.id
                        self.blocks[file.block.start + i] = -1
                        self.moved_ids.add(file.id)
                    # print(self.blocks)
                    continue
        return False

    def check_sum(self) -> int:
        values = [idx * file_id for idx, file_id in enumerate(self.blocks) if file_id != -1]
        return sum(values)

    @timer
    def part2(self):
        self.defragment_step()
        print(self.blocks)
        return self.check_sum()


part2 = Day09(lines[0]).part2()
print(f"part2: {part2}")
