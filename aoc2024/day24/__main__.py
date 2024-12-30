from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from typing import Callable, Iterable, Optional

import networkx as nwx
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import split_by
from aoc2024.utils.mynumpy import Matrix, Pos2D
from aoc2024.utils.reader import read_input

type Cell = tuple[int, int]
type BlockSourceTarget = tuple[Cell, Cell, Cell]


IS_TEST = False

lines = read_input(IS_TEST)

type Input = dict[str, int]


@dataclass
class Operation:
    input1: str
    input2: str
    op: Callable[[int, int], int]
    output: str


def and_op(a: int, b: int) -> int:
    return a & b


def or_op(a: int, b: int) -> int:
    return a | b


def xor_op(a: int, b: int) -> int:
    return a ^ b


op_map = {
    "AND": and_op,
    "OR": or_op,
    "XOR": xor_op,
}

register_ops: dict[str, list[Operation]] = defaultdict(list)


def process_lines() -> tuple[Input, list[Operation]]:
    input_lines, op_lines = split_by(lines, "")
    inputs = {}
    for value in input_lines:
        name, value = value.split(": ")
        inputs[name] = int(value)
    operations = []
    for operation in op_lines:
        input1, op_str, input2, _, output = operation.split()
        op = op_map[op_str]
        operation = Operation(input1, input2, op, output)
        register_ops[input1].append(operation)
        register_ops[input2].append(operation)
        operations.append(operation)
    return inputs, operations


registers: dict[str, int] = {}


def set_register(name: str, value: int) -> None:
    registers[name] = value
    for operation in register_ops[name]:
        input1 = registers.get(operation.input1, None)
        input2 = registers.get(operation.input2, None)
        if input1 is not None and input2 is not None:
            set_register(operation.output, operation.op(input1, input2))


def part1() -> None:
    inputs, operations = process_lines()
    for reg, val in inputs.items():
        set_register(reg, val)
    zregs = [
        (reg, val)
        for reg, val in registers.items()
        if reg.startswith("z")
        #
    ]
    binary = "".join([str(val) for _, val in reversed(sorted(zregs))])
    print(int(binary, 2))


part1()
