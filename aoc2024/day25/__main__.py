from typing import NamedTuple
from aoc2024.utils.collections import partition, split_by
from aoc2024.utils.mynumpy import Matrix
from aoc2024.utils.reader import read_input


IS_TEST = False
lines = read_input(IS_TEST)


class LockKey(NamedTuple):
    is_lock: bool
    pattern: list[int]


def create_matrices() -> list[Matrix]:
    blocks = split_by(lines, "")
    return [Matrix.from_lines(block) for block in blocks]


def create_lock_key(matrix: Matrix) -> LockKey:
    is_lock = (matrix[0] == "#").all().item()
    pattern = [(matrix[:, i] == "#").sum().item() - 1 for i in range(matrix.shape[1])]
    return LockKey(is_lock, pattern)


def part1() -> None:
    matrices = create_matrices()
    lock_keys = [create_lock_key(matrix) for matrix in matrices]
    locks, keys = partition(lock_keys, lambda lk: lk.is_lock)
    result = 0
    for lock in locks:
        for key in keys:
            sums = [l + k for l, k in zip(lock.pattern, key.pattern)]
            if all(s < 6 for s in sums):
                result += 1
    print(f"Part1: {result}")


if __name__ == "__main__":
    part1()
