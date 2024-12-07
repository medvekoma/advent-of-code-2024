import re
from operator import add, mul
from itertools import product
from functools import lru_cache
from typing import Optional
from aoc2024.utils.collections import partition
from aoc2024.utils.reader import read_lines
from aoc2024.utils.timer import timer

lines = read_lines(is_test=False)

input_strings = [re.findall(r"\d+", line) for line in lines]
input_numbers = [[int(s) for s in strings] for strings in input_strings]


def operator_lists(length: int, operators: list):
    yield from product(operators, repeat=length)


def test_line(numbers: list[int], operators: list) -> bool:
    expected_result = numbers[0]
    first_num = numbers[1]
    next_numbers = numbers[2:]
    for ops in operator_lists(len(next_numbers), operators):
        result = first_num
        for op, num in zip(ops, next_numbers):
            result = op(result, num)
            # if result > expected_result:
            #     break
        if result == expected_result:
            return True
    return False


@lru_cache(maxsize=1024)
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

    good_lines2 = [line for line in bad_lines if test_line(line, [add, mul, concat])]
    result2 = result1 + sum(line[0] for line in good_lines2)
    print(f"part2: {result2}")


parts()
