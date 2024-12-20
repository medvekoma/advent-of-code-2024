from collections import defaultdict
from math import prod
from typing import Iterable

import numpy as np
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import group_list, parse_ints
from aoc2024.utils.reader import read_lines

IS_TEST = False

lines = read_lines(IS_TEST)


class Day:
    def __init__(self) -> None:
        self.A = "a"
        self.B = "0"
        self.C = "0"
        self.program = parse_ints(lines[4])
        self.pointer = 0
        self.ops = {
            0: self.adv,
            6: self.bdv,
            7: self.cdv,
            1: self.bxl,
            2: self.bst,
            4: self.bxc,
            3: self.jnz,
            5: self.out,
        }

    def combo(self, operand: int) -> str:
        if operand in [0, 1, 2, 3]:
            return str(operand)
        if operand == 4:
            return f"({self.A})"
        if operand == 5:
            return f"({self.B})"
        if operand == 6:
            return f"({self.C})"
        raise ValueError(f"Invalid combo {operand}")

    def adv(self, operand: int) -> None:
        self.A = f"({self.A}) // (2 ** {self.combo(operand)})"

    def bxl(self, operand: int) -> None:
        self.B = f"({self.B}) ^ {operand}"

    def bst(self, operand: int) -> None:
        self.B = f"({self.combo(operand)}) % 8"

    def jnz(self, operand: int) -> None:
        pass
        # if self.A != 0:
        #     self.pointer = operand - 2  # -2 because we will add 2 in the processing loop

    def bxc(self, _: int) -> None:
        self.B = f"({self.B}) ^ ({self.C})"

    def out(self, operand: int) -> str:
        print(f"OUT: ({self.combo(operand)}) % 8")

    def bdv(self, operand: int) -> None:
        self.B = f"({self.A}) // (2 ** {self.combo(operand)})"

    def cdv(self, operand: int) -> None:
        self.C = f"({self.A}) // (2 ** {self.combo(operand)})"

    def part2(self) -> None:
        while self.pointer < len(self.program):
            opcode, operand = self.program[self.pointer], self.program[self.pointer + 1]
            operator = self.ops[opcode]
            # print(operator.__name__, operand)
            operator(operand)
            self.pointer += 2
        print(self.A)
        print(self.B)
        print(self.C)

    def digit_map(self, n: int) -> Iterable[dict[int, int]]:
        for mod in range(8):
            res: dict[int, int] = defaultdict(set)
            last_bits = reversed("{:03b}".format(mod))
            for i, bit in enumerate(last_bits):
                res[i].add(int(bit))
            first_bits = reversed("{:03b}".format(mod ^ n))
            offset = 7 - mod
            for i, bit in enumerate(first_bits):
                res[offset + i].add(int(bit))
            overlaps = {k for k, v in res.items() if len(v) > 1}
            # print(">", mod, first_bits, last_bits, res)
            if not overlaps:
                yield res

    def xxx(self):
        for a in range(8):
            out = ((a % 8) ^ (a // (2 ** ((a % 8) ^ 7)))) % 8
            a_mod_8 = {  #                                                           - 9876543210
                0: (0 ^ (a // (2**7))) % 8,  # xxx??????? - digits as they are              - xxx????000 - 010....000
                1: (1 ^ (a // (2**6))) % 8,  # ?xxx?????? - reverts last digit              - ?xxx???001 - .011...001
                2: (2 ^ (a // (2**5))) % 8,  # ??xxx????? - reverts middle digit            - ??xxx??010 - ..000..010
                3: (3 ^ (a // (2**4))) % 8,  # ???xxx???? - reverts last two digits         - ???xxx?011 - ...001.011
                4: (4 ^ (a // (2**3))) % 8,  # ????xxx??? - reverts first digit             - ????xxx100 - ....110100
                5: (5 ^ (a // (2**2))) % 8,  # ?????xxx?? - reverts first and last digits   - ?????xx101 - .....11101
                6: (6 ^ (a // (2**1))) % 8,  # ??????xxx? - reverts first and middle digits - ??????x110 - ......100 !
                7: (7 ^ (a // (2**0))) % 8,  # ???????xxx - reverts all 3 digits            - ???????111 - .......101!
            }


def parts():
    day = Day()
    for m in day.digit_map(2):
        print(m)


parts()
