import numpy as np
from aoc2024.utils.reader import read_lines


lines = read_lines(is_test=False)

matrix = np.array([list(line) for line in lines])
rows, cols = matrix.shape


def get_diagonals(matrix_):
    rows_, cols_ = matrix_.shape
    return [
        "".join(matrix_.diagonal(offset)) for offset in range(cols_ - 1, -rows_, -1)
    ]


def get_lines():
    horizontal = ["".join(row) for row in matrix]
    horizontal_back = [line[::-1] for line in horizontal]
    diagonals = get_diagonals(matrix)
    diagonals_back = [line[::-1] for line in diagonals]
    vertical = ["".join(row) for row in matrix.T]
    vertical_back = [line[::-1] for line in vertical]
    anti_diagonals = get_diagonals(np.fliplr(matrix))
    anti_diagonals_back = [line[::-1] for line in anti_diagonals]
    return (
        horizontal
        + horizontal_back
        + diagonals
        + diagonals_back
        + vertical
        + vertical_back
        + anti_diagonals
        + anti_diagonals_back
    )


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
