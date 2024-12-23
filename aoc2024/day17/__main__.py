from collections import defaultdict
from typing import Iterable, Optional

from aoc2024.utils.collections import parse_ints
from aoc2024.utils.reader import read_input

IS_TEST = False

lines = read_input(IS_TEST)


class Computer:
    def __init__(self) -> None:
        self.a = parse_ints(lines[0])[0]
        self.b = parse_ints(lines[1])[0]
        self.c = parse_ints(lines[2])[0]
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

    def reinit(self, a: int) -> None:
        self.a = a
        self.b = 0
        self.c = 0
        self.pointer = 0

    def combo(self, operand: int) -> int:
        if operand in [0, 1, 2, 3]:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        raise ValueError(f"Invalid combo {operand}")

    def adv(self, operand: int) -> None:
        denominator = pow(2, self.combo(operand))
        self.a = self.a // denominator

    def bxl(self, operand: int) -> None:
        self.b = self.b ^ operand

    def bst(self, operand: int) -> None:
        self.b = self.combo(operand) % 8

    def jnz(self, operand: int) -> None:
        if self.a != 0:
            self.pointer = operand - 2  # -2 because we will add 2 in the processing loop

    def bxc(self, _: int) -> None:
        self.b = self.b ^ self.c

    def out(self, operand: int) -> str:
        return str(self.combo(operand) % 8)

    def bdv(self, operand: int) -> None:
        denominator = pow(2, self.combo(operand))
        self.b = self.a // denominator

    def cdv(self, operand: int) -> None:
        denominator = pow(2, self.combo(operand))
        self.c = self.a // denominator

    def run(self) -> str:
        results = []
        while self.pointer < len(self.program):
            opcode, operand = self.program[self.pointer], self.program[self.pointer + 1]
            operator = self.ops[opcode]
            # print(operator.__name__, operand)
            results.append(operator(operand))
            self.pointer += 2
        output = ",".join(res for res in results if res is not None)
        return output


def part1() -> None:
    computer = Computer()
    output = computer.run()
    print(f"Part 1: {output}")


def decoded_step(a: int) -> tuple[int, int]:
    """
    Decoded program, executes one iteration, returns A and output
    """
    a1 = a // 8
    # b1 = (a % 8) ^ (a // (2 ** ((a % 8) ^ 7)))
    # c1 = a // (2 ** ((a % 8) ^ 7))
    out = ((a % 8) ^ (a // (2 ** ((a % 8) ^ 7)))) % 8
    return a1, out


def decoded_program(a: int) -> str:
    """
    Decoded program, executes all iterations, returns output
    """
    outputs = []
    while a != 0:
        a, out = decoded_step(a)
        outputs.append(str(out))
    return ",".join(outputs)


def digit_map(n: int) -> Iterable[dict[int, int]]:
    """
    Reversed step: for any output number, returns the possible bit values (position: value)
    """
    for mod in range(8):
        res: dict[int, set[int]] = defaultdict(set)
        last_bits = reversed(f"{mod:03b}")
        for i, bit in enumerate(last_bits):
            res[i].add(int(bit))
        first_bits = reversed(f"{mod ^ n:03b}")
        offset = 7 - mod
        for i, bit in enumerate(first_bits):
            res[offset + i].add(int(bit))
        overlaps = {k for k, v in res.items() if len(v) > 1}
        # print(">", mod, first_bits, last_bits, res)
        if not overlaps:
            yield {k: list(v)[0] for k, v in res.items()}


def shift_maps(maps: Iterable[dict[int, int]], digits: int) -> Iterable[dict[int, int]]:
    for m in maps:
        new_map = {k + digits: v for k, v in m.items()}
        yield new_map


def merge_map(map1: dict[int, int], map2: dict[int, int]) -> Optional[dict[int, int]]:
    """
    Combines two digit maps, returns the merged map if possible, None otherwise
    """
    all_keys = set(map1.keys()) | set(map2.keys())
    result = {}
    for key in all_keys:
        v1 = map1.get(key, None)
        v2 = map2.get(key, None)
        if v1 is not None and v2 is not None and v1 != v2:
            return None
        result[key] = v1 or v2 or 0  # at least one of them is not None
    return result


def merge_maps(maps1: Iterable[dict[int, int]], maps2: Iterable[dict[int, int]]) -> Iterable[dict[int, int]]:
    for map1 in maps1:
        for map2 in maps2:
            merged_map = merge_map(map1, map2)
            if merged_map:
                yield merged_map


def get_value(postion_map: dict[int, int]) -> int:
    """
    Converts a binary digit map to an integer
    """
    max_key = max(postion_map.keys())
    buffer = ["0"] * (max_key + 1)
    for k, v in postion_map.items():
        buffer[max_key - k] = str(v)
    binary = "".join(buffer)
    return int(binary, 2)


def part2() -> None:
    computer = Computer()
    maps: Iterable[dict[int, int]] = []
    for i, num in enumerate(computer.program):
        current_maps = list(digit_map(num))
        if not maps:
            maps = current_maps
        else:
            current_maps = list(shift_maps(current_maps, i * 3))
            maps = list(merge_maps(maps, current_maps))
    values = [get_value(rolling_map) for rolling_map in maps]
    print(f"Part 2: {min(values)}")


def parts():
    part1()
    part2()


if __name__ == "__main__":
    parts()
