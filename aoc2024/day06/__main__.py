from typing import Optional
import numpy as np
from aoc2024.utils.reader import read_lines

lines = read_lines(is_test=False)

array = [list(line) for line in lines]
matrix1 = np.array(array)
matrix = np.pad(matrix1, pad_width=1)
position = tuple(np.argwhere(matrix == "^")[0])
original_position = position
orientation = (-1, 0)
matrix[position] = "."


def add(a: tuple, b: tuple) -> tuple:
    return tuple(map(sum, zip(a, b)))


def rotate(ori: tuple, clockwise: bool = True) -> tuple:
    if clockwise:
        return ori[1], -ori[0]
    return -ori[1], ori[0]


def move_if_possible(mtx: np.ndarray, pos: tuple, ori: tuple) -> Optional[tuple]:
    new_pos = add(pos, ori)
    if mtx[new_pos] == "#":
        return None
    return new_pos


def move(mtx: np.ndarray, pos: tuple, ori: tuple) -> tuple[tuple, tuple]:
    new_pos = move_if_possible(mtx, pos, ori)
    if new_pos:
        return (new_pos, ori)
    new_ori = rotate(ori)
    return move(mtx, pos, new_ori)


def part1():
    pos, ori = position, orientation
    positions = {position}
    while True:
        pos, ori = move(matrix, pos, ori)
        if matrix[pos] == "0":
            break
        positions.add(pos)
    return len(positions)


def is_in_loop(
    mtx: np.ndarray,
    visited_pairs: set[tuple[tuple, tuple]],
    pos: tuple,
    ori: tuple,
    next_pos: tuple,
) -> bool:
    if next_pos == original_position:
        return False
    new_mtx = mtx.copy()
    new_mtx[next_pos] = "#"
    pairs = visited_pairs.copy()
    while True:
        pos, ori = move(new_mtx, pos, ori)
        if matrix[pos] == "0":
            return False
        pair = (pos, ori)
        if pair in pairs:
            return True
        pairs.add(pair)


def part2():
    pos, ori = position, orientation
    positions = {position}
    pairs = {(position, orientation)}
    checked_positions = set()
    blockers = set()
    while True:
        new_pos, new_ori = move(matrix, pos, ori)
        if matrix[new_pos] == "0":
            break
        if new_pos not in checked_positions and is_in_loop(matrix, pairs, pos, ori, new_pos):
            blockers.add(new_pos)
        checked_positions.add(new_pos)
        pos, ori = new_pos, new_ori
        positions.add(pos)
        pairs.add((pos, ori))
    return (len(positions), len(blockers))


# print(f"part1: {part1()}")
print(f"part2: {part2()}")
