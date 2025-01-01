from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

from aoc2024.utils.collections import split_by
from aoc2024.utils.reader import read_input


IS_TEST = False
REGISTER_COUNT = 46

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


class Operators:
    @staticmethod
    def and_op(a: int, b: int) -> int:
        return a & b

    @staticmethod
    def or_op(a: int, b: int) -> int:
        return a | b

    @staticmethod
    def xor_op(a: int, b: int) -> int:
        return a ^ b

    from_name = {
        "AND": and_op,
        "OR": or_op,
        "XOR": xor_op,
    }

    to_symbol: dict[Callable[[int, int], int], str] = {
        and_op: "&",
        or_op: "|",
        xor_op: "^",
    }


class Day24:
    def __init__(self) -> None:
        self.init_values: dict[str, int] = {}
        self.registers: dict[str, int] = {}
        self.ops_by_input: dict[str, list[Operation]] = defaultdict(list)
        self.op_by_output: dict[str, Operation] = {}

        init_lines, op_lines = split_by(lines, "")
        for init_line in init_lines:
            name, value = init_line.split(": ")
            self.init_values[name] = int(value)

        for op_line in op_lines:
            input1, op_str, input2, _, output = op_line.split()
            op_func = Operators.from_name[op_str]
            operation = Operation(Expression({input1, input2}, op_func), output)
            self.ops_by_input[input1].append(operation)
            self.ops_by_input[input2].append(operation)
            self.op_by_output[output] = operation

    def set_register(self, name: str, value: int) -> None:
        self.registers[name] = value
        for operation in self.ops_by_input[name]:
            expression = operation.expression
            input1, input2 = expression.inputs
            value1 = self.registers.get(input1, None)
            value2 = self.registers.get(input2, None)
            if value1 is not None and value2 is not None:
                self.set_register(operation.output, expression.op(value1, value2))

    def part1(self) -> None:
        for reg, val in self.init_values.items():
            self.set_register(reg, val)
        zregs = [
            (reg, val)
            for reg, val in self.registers.items()
            if reg.startswith("z")
            #
        ]
        binary = "".join([str(val) for _, val in reversed(sorted(zregs))])
        print(f"Part 1: {int(binary, 2)}")

    def reg_expression(self, reg: str) -> str:
        if reg not in self.op_by_output:
            return reg
        operation = self.op_by_output[reg]
        input1, input2 = operation.expression.inputs
        exp1 = self.reg_expression(input1)
        exp2 = self.reg_expression(input2)
        if len(exp1) > 3:
            exp1 = f"({exp1})"
        if len(exp2) > 3:
            exp2 = f"({exp2})"
        return f"{exp1} {Operators.to_symbol[operation.expression.op]} {exp2}"

    def dump_expressions(self) -> None:
        for i in range(REGISTER_COUNT):
            reg = f"z{i:02}"
            exp = self.reg_expression(reg)
            print(f"{reg}: {exp}")


if __name__ == "__main__":
    day24 = Day24()
    day24.part1()
    day24.dump_expressions()
