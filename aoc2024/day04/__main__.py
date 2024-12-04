import numpy as np
from aoc2024.utils.reader import read_lines


lines = read_lines()

matrix = np.array([list(line) for line in lines])
rows, cols = matrix.shape


def get_diagonals(matrix_param):
    rows_param, cols_param = matrix_param.shape
    return [
        "".join(matrix_param.diagonal(offset))
        for offset in range(-rows_param + 1, cols_param)
    ]


def get_lines():
    horizontal = ["".join(row) for row in matrix]
    vertical = ["".join(row) for row in matrix.T]
    diagonals = get_diagonals(matrix)
    anti_diagonals = get_diagonals(np.fliplr(matrix))

    one_way = horizontal + diagonals + vertical + anti_diagonals

    return one_way + [line[::-1] for line in one_way]


def part1():
    all_lines = get_lines()
    matches = [line.count("XMAS") for line in all_lines]
    return sum(matches)


def is_xmas(r: int, c: int) -> bool:
    if r < 1 or r >= rows - 1 or c < 1 or c >= cols - 1:
        return False
    if matrix[r, c] != "A":
        return False
    if {matrix[r - 1, c - 1], matrix[r + 1, c + 1]} != {"M", "S"}:
        return False
    if {matrix[r - 1, c + 1], matrix[r + 1, c - 1]} != {"M", "S"}:
        return False
    return True


def part2():
    indices = [(r, c) for r in range(rows) for c in range(cols) if is_xmas(r, c)]
    return len(indices)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
