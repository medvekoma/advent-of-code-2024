import re
from operator import add, mul
from itertools import product
from typing import Callable, Iterable
from aoc2024.utils.collections import partition
from aoc2024.utils.reader import read_lines
from aoc2024.utils.benchmark import timer

lines = read_lines(is_test=False)
type Operator = Callable[[int, int], int]

input_strings = [re.findall(r"\d+", line) for line in lines]
input_numbers = [[int(s) for s in strings] for strings in input_strings]


def operators_permutations(length: int, operators: list[Operator]) -> Iterable[tuple[Operator]]:
    yield from product(operators, repeat=length)


def test_line(numbers: list[int], operators: list[Operator]) -> bool:
    expected_result = numbers[0]
    first_num = numbers[1]
    next_numbers = numbers[2:]
    for ops in operators_permutations(len(next_numbers), operators):
        result = first_num
        for op, num in zip(ops, next_numbers):
            result = op(result, num)
        if result == expected_result:
            return True
    return False


def concat(a: int, b: int) -> int:
    # return int(str(a) + str(b))
    # hacks for more efficient concatenation
    if b < 10:
        return a * 10 + b
    if b < 100:
        return a * 100 + b
    if b < 1000:
        return a * 1000 + b
    return a * 10 ** len(str(b)) + b


@timer
def parts():
    good_lines, bad_lines = partition(input_numbers, lambda line: test_line(line, [add, mul]))

    result1 = sum(line[0] for line in good_lines)
    print(f"part1: {result1}")

    good_lines = [line for line in bad_lines if test_line(line, [concat, add, mul])]
    result2 = result1 + sum(line[0] for line in good_lines)
    print(f"part2: {result2}")


parts()
