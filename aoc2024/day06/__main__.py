from typing import Optional
from aoc2024.utils.reader import read_lines
from aoc2024.utils.timer import timer

lines = read_lines(is_test=False)
type Cell = tuple[int, int]
type Orientation = tuple[int, int]

rows = len(lines)
cols = len(lines[0])
obstructions: set[Cell] = set()
position: Cell = (0, 0)
for r in range(rows):
    for c in range(cols):
        if lines[r][c] == "#":
            obstructions.add((r, c))
        if lines[r][c] == "^":
            position = (r, c)
original_position = position
orientation = (-1, 0)


def step(a: Cell, b: Orientation) -> Cell:
    return a[0] + b[0], a[1] + b[1]


def turn_right(ori: Orientation) -> Orientation:
    return ori[1], -ori[0]


def move_if_possible(obsts: set[Cell], pos: Cell, ori: Orientation) -> Optional[Cell]:
    new_pos = step(pos, ori)
    if new_pos in obsts:
        return None
    return new_pos


def move(obsts: set[Cell], pos: Cell, ori: Orientation) -> tuple[Cell, Orientation]:
    while not (new_pos := move_if_possible(obsts, pos, ori)):
        ori = turn_right(ori)
    return new_pos, ori


def is_outside(pos: Cell) -> bool:
    return pos[0] < 0 or pos[0] >= rows or pos[1] < 0 or pos[1] >= cols


def is_in_loop(
    visited_pairs: set[tuple[Cell, Orientation]],
    pos: Cell,
    ori: Orientation,
    next_pos: Cell,
) -> bool:
    _obstructions = obstructions | {next_pos}
    new_pairs = set()
    while True:
        pos, ori = move(_obstructions, pos, ori)
        if is_outside(pos):
            return False
        pair = (pos, ori)
        if pair in visited_pairs or pair in new_pairs:
            return True
        new_pairs.add(pair)


@timer
def parts():
    visited_positions = {position}
    visited_pairs = {(position, orientation)}
    checked_blockers = set(original_position)
    blockers = set()
    pos, ori = position, orientation
    while True:
        new_pos, new_ori = move(obstructions, pos, ori)
        if is_outside(new_pos):
            break
        if new_pos not in checked_blockers:
            if is_in_loop(visited_pairs, pos, ori, new_pos):
                blockers.add(new_pos)
            checked_blockers.add(new_pos)
        pos, ori = new_pos, new_ori
        visited_positions.add(pos)
        visited_pairs.add((pos, ori))
    return (len(visited_positions), len(blockers))


print(f"parts: {parts()}")
