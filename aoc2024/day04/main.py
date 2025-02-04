import numpy as np
from aoc2024.utils.mynumpy import Matrix
from aoc2024.utils.reader import read_input


lines = read_input()

matrix = Matrix.from_lines(lines)
rows, cols = matrix.shape


def get_diagonals(matrix_param):
    rows_param, cols_param = matrix_param.shape
    # by adding 3 to the range limits we can skip the items shorter than 4
    return ["".join(matrix_param.diagonal(offset)) for offset in range(-rows_param + 4, cols_param - 3)]


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
    if matrix[r, c] != "A":
        return False
    if {matrix[r - 1, c - 1], matrix[r + 1, c + 1]} != {"M", "S"}:
        return False
    if {matrix[r - 1, c + 1], matrix[r + 1, c - 1]} != {"M", "S"}:
        return False
    return True


def part2():
    indices = [(row, col) for row in range(1, rows - 1) for col in range(1, cols - 1) if is_xmas(row, col)]
    return len(indices)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
