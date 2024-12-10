import numpy as np
from aoc2024.utils.collections import digit_matix, get_neighbors
from aoc2024.utils.reader import read_lines

lines = read_lines(is_test=False)

matrix = digit_matix(lines)

type Cell = tuple[int, int]


def collect_trail_heads() -> list[Cell]:
    trail_heads_where = np.where(matrix == 0)
    trail_heads = [(int(r), int(c)) for r, c in zip(*trail_heads_where)]
    return trail_heads


def count_paths(cell: Cell) -> int:
    value = matrix[cell]
    if value == 9:
        return 1
    good_neighbors = [n for n in get_neighbors(matrix, cell) if matrix[n] == value + 1]
    return sum(count_paths(n) for n in good_neighbors)


def collect_trail_ends(cell: Cell) -> set[Cell]:
    value = matrix[cell]
    if value == 9:
        return {cell}
    good_neighbors = [n for n in get_neighbors(matrix, cell) if matrix[n] == value + 1]
    return {trail_end for neighbor in good_neighbors for trail_end in collect_trail_ends(neighbor)}


def parts():
    trail_heads = collect_trail_heads()
    trail_ends = [len(collect_trail_ends(trail_head)) for trail_head in trail_heads]
    print(f"part1: {sum(trail_ends)}")
    paths = [count_paths(trail_head) for trail_head in trail_heads]
    print(f"part2: {sum(paths)}")


parts()
