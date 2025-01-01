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

type Registers = dict[str, int]


@dataclass
class Expression:
    inputs: set[str]
    op: Callable[[int, int], int]


@dataclass
class Operation:
    expression: Expression
    output: str


type RegisterOperations = dict[str, list[Operation]]


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


class Day24:
    def __init__(self) -> None:
        self.inputs = {}
        self.register_ops: RegisterOperations = defaultdict(list)
        self.registers: dict[str, int] = {}
        self.output_dict: dict[str, Operation] = {}

        input_lines, op_lines = split_by(lines, "")
        for value in input_lines:
            name, value = value.split(": ")
            self.inputs[name] = int(value)

        for op_line in op_lines:
            input1, op_str, input2, _, output = op_line.split()
            op_func = op_map[op_str]
            operation = Operation(Expression({input1, input2}, op_func), output)
            self.register_ops[input1].append(operation)
            self.register_ops[input2].append(operation)
            self.output_dict[output] = operation

    def set_register(self, name: str, value: int) -> None:
        self.registers[name] = value
        for operation in self.register_ops[name]:
            expression = operation.expression
            input1, input2 = expression.inputs
            value1 = self.registers.get(input1, None)
            value2 = self.registers.get(input2, None)
            if value1 is not None and value2 is not None:
                self.set_register(operation.output, expression.op(value1, value2))

    def part1(self) -> None:
        for reg, val in self.inputs.items():
            self.set_register(reg, val)
        zregs = [
            (reg, val)
            for reg, val in self.registers.items()
            if reg.startswith("z")
            #
        ]
        binary = "".join([str(val) for _, val in reversed(sorted(zregs))])
        print(f"Part 1: {int(binary, 2)}")

    op_dict: dict[Callable[[int, int], int], str] = {
        and_op: "&",
        or_op: "|",
        xor_op: "^",
    }

    def reg_expression(self, reg: str) -> str:
        if reg not in self.output_dict:
            return reg
        operation = self.output_dict[reg]
        input1, input2 = operation.expression.inputs
        exp1 = self.reg_expression(input1)
        exp2 = self.reg_expression(input2)
        if len(exp1) > 3:
            exp1 = f"({exp1})"
        if len(exp2) > 3:
            exp2 = f"({exp2})"
        return f"{exp1} {self.op_dict[operation.expression.op]} {exp2}"

    def expressions(self) -> None:
        for i in range(46):
            reg = f"z{i:02}"
            exp = self.reg_expression(reg)
            print(f"{reg}: {exp}")


if __name__ == "__main__":
    day24 = Day24()
    day24.part1()
    day24.expressions()
