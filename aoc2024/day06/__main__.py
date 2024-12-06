from typing import Optional
import numpy as np
from aoc2024.utils.reader import read_lines

lines = read_lines(is_test=True)

array = [list(line) for line in lines]
matrix1 = np.array(array)
matrix = np.pad(matrix1, pad_width=1)
position = tuple(np.argwhere(matrix == "^")[0])
direction = (-1, 0)
matrix[position] = "."


def add(a: tuple, b: tuple) -> tuple:
    return tuple(map(sum, zip(a, b)))


def rotate(dir: tuple, clockwise: bool = True) -> tuple:
    if clockwise:
        return dir[1], -dir[0]
    return -dir[1], dir[0]


def move_if_possible(pos: tuple, dir: tuple) -> Optional[tuple]:
    new_pos = add(pos, dir)
    if matrix[new_pos] == "#":
        return None
    return new_pos


def move(pos: tuple, dir: tuple) -> tuple[tuple, tuple]:
    new_pos = move_if_possible(pos, dir)
    if new_pos:
        return (new_pos, dir)
    new_dir = rotate(dir)
    return move(pos, new_dir)


def part1():
    pos, dir = position, direction
    positions = {position}
    while True:
        pos, dir = move(pos, dir)
        if matrix[pos] == "0":
            break
        positions.add(pos)
    return len(positions)


def part2():
    pass


print(f"part1: {part1()}")
print(f"part2: {part2()}")
