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
    op: str
    inputs: frozenset[str]


@dataclass
class Operation:
    expression: Expression
    output: str


class Operators:
    @staticmethod
    def and_func(a: int, b: int) -> int:
        return a & b

    @staticmethod
    def or_func(a: int, b: int) -> int:
        return a | b

    @staticmethod
    def xor_func(a: int, b: int) -> int:
        return a ^ b

    to_func = {
        "AND": and_func,
        "OR": or_func,
        "XOR": xor_func,
    }

    @staticmethod
    def func(op: str, a: int, b: int) -> int:
        return Operators.to_func[op](a, b)

    to_symbol: dict[str, str] = {
        "AND": "&",
        "OR": "|",
        "XOR": "^",
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
            expression = Expression(op_str, frozenset({input1, input2}))
            operation = Operation(expression, output)
            self.ops_by_input[input1].append(operation)
            self.ops_by_input[input2].append(operation)
            self.op_by_output[output] = operation

    def set_register(self, name: str, value: int) -> None:
        self.registers[name] = value
        for operation in self.ops_by_input[name]:
            expression = operation.expression
            value1, value2 = [self.registers.get(input, None) for input in expression.inputs]
            if value1 is not None and value2 is not None:
                new_value = Operators.func(expression.op, value1, value2)
                self.set_register(operation.output, new_value)

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
