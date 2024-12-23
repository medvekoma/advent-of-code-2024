from aoc2024.utils.collections import parse_ints
from aoc2024.utils.reader import read_input

IS_TEST = False

lines = read_input(IS_TEST)


class LiteralComputer:
    # pylint: disable=duplicate-code
    def __init__(self) -> None:
        self.a = "a"
        self.b = "0"
        self.c = "0"
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
            return f"({self.a})"
        if operand == 5:
            return f"({self.b})"
        if operand == 6:
            return f"({self.c})"
        raise ValueError(f"Invalid combo {operand}")

    def adv(self, operand: int) -> None:
        self.a = f"({self.a}) // (2 ** {self.combo(operand)})"

    def bxl(self, operand: int) -> None:
        self.b = f"({self.b}) ^ {operand}"

    def bst(self, operand: int) -> None:
        self.b = f"({self.combo(operand)}) % 8"

    def jnz(self, operand: int) -> None:
        """Jump if not zero, doesn't affect registers"""

    def bxc(self, _: int) -> None:
        self.b = f"({self.b}) ^ ({self.c})"

    def out(self, operand: int) -> None:
        print(f"OUT: ({self.combo(operand)}) % 8")

    def bdv(self, operand: int) -> None:
        self.b = f"({self.a}) // (2 ** {self.combo(operand)})"

    def cdv(self, operand: int) -> None:
        self.c = f"({self.a}) // (2 ** {self.combo(operand)})"

    def part2(self) -> None:
        while self.pointer < len(self.program):
            opcode, operand = self.program[self.pointer], self.program[self.pointer + 1]
            operator = self.ops[opcode]
            operator(operand)
            self.pointer += 2
        print(self.a)
        print(self.b)
        print(self.c)

    # output_expression = ((a % 8) ^ (a // (2 ** ((a % 8) ^ 7)))) % 8
    # a_mod_8 = {  #                     9876543210
    #     0: (0 ^ (a // (2**7))) % 8,  # xxx....000
    #     1: (1 ^ (a // (2**6))) % 8,  # .xxx...001
    #     2: (2 ^ (a // (2**5))) % 8,  # ..xxx..010
    #     3: (3 ^ (a // (2**4))) % 8,  # ...xxx.011
    #     4: (4 ^ (a // (2**3))) % 8,  # ....xxx100
    #     5: (5 ^ (a // (2**2))) % 8,  # .....xx101
    #     6: (6 ^ (a // (2**1))) % 8,  # ......x110
    #     7: (7 ^ (a // (2**0))) % 8,  # .......111
    # }


if __name__ == "__main__":
    LiteralComputer().part2()
