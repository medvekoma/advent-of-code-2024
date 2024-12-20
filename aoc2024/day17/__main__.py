from collections import defaultdict
from math import prod
from typing import Iterable, Optional

import numpy as np
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import group_list, parse_ints
from aoc2024.utils.reader import read_lines

IS_TEST = False

lines = read_lines(IS_TEST)


class Day:
    def __init__(self) -> None:
        self.A = parse_ints(lines[0])[0]
        self.B = parse_ints(lines[1])[0]
        self.C = parse_ints(lines[2])[0]
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
        self.A = a
        self.B = 0
        self.C = 0
        self.pointer = 0

    def combo(self, operand: int) -> int:
        if operand in [0, 1, 2, 3]:
            return operand
        if operand == 4:
            return self.A
        if operand == 5:
            return self.B
        if operand == 6:
            return self.C
        raise ValueError(f"Invalid combo {operand}")

    def adv(self, operand: int) -> None:
        denominator = pow(2, self.combo(operand))
        self.A = self.A // denominator

    def bxl(self, operand: int) -> None:
        self.B = self.B ^ operand

    def bst(self, operand: int) -> None:
        self.B = self.combo(operand) % 8

    def jnz(self, operand: int) -> None:
        if self.A != 0:
            self.pointer = operand - 2  # -2 because we will add 2 in the processing loop

    def bxc(self, _: int) -> None:
        self.B = self.B ^ self.C

    def out(self, operand: int) -> str:
        return str(self.combo(operand) % 8)

    def bdv(self, operand: int) -> None:
        denominator = pow(2, self.combo(operand))
        self.B = self.A // denominator

    def cdv(self, operand: int) -> None:
        denominator = pow(2, self.combo(operand))
        self.C = self.A // denominator

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

    def part1(self) -> None:
        output = self.run()
        print(f"Part 1: {output}")

    def cycle(self, a: int) -> tuple[int, int]:
        a1 = a // 8
        # b1 = (a % 8) ^ (a // (2 ** ((a % 8) ^ 7)))
        # c1 = a // (2 ** ((a % 8) ^ 7))
        out = ((a % 8) ^ (a // (2 ** ((a % 8) ^ 7)))) % 8
        return a1, out

    def compiled(self, a: int) -> str:
        outputs = []
        while a != 0:
            a, out = self.cycle(a)
            outputs.append(str(out))
        return ",".join(outputs)

    def part1b(self) -> None:
        output = self.compiled(self.A)
        print(f"Part 1: {output}")

    def digit_map(n: int) -> Iterable[dict[int, int]]:
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
                yield {k: list(v)[0] for k, v in res.items()}

    def shift_maps(maps: Iterable[dict[int, int]], digits: int) -> Iterable[dict[int, int]]:
        for map in maps:
            new_map = {k + digits: v for k, v in map.items()}
            yield new_map

    def merge_map(map1: dict[int, int], map2: dict[int, int]) -> Optional[dict[int, int]]:
        all_keys = set(map1.keys()) | set(map2.keys())
        result = {}
        for key in all_keys:
            v1 = map1.get(key, None)
            v2 = map2.get(key, None)
            if v1 is not None and v2 is not None and v1 != v2:
                return None
            result[key] = v1 if v1 is not None else v2
        return result

    def merge_maps(maps1: Iterable[dict[int, int]], maps2: Iterable[dict[int, int]]) -> Iterable[dict[int, int]]:
        for map1 in maps1:
            for map2 in maps2:
                merged_map = Day.merge_map(map1, map2)
                if merged_map:
                    yield merged_map

    def get_value(postion_map: dict[int, int]) -> int:
        # print(postion_map)
        max_key = max(postion_map.keys())
        buffer = ["0"] * (max_key + 1)
        for k, v in postion_map.items():
            buffer[max_key - k] = str(v)
        binary = "".join(buffer)
        print(binary)
        return int(binary, 2)

    def test() -> None:
        day = Day()
        maps = list(Day.digit_map(day.program[0]))
        maps1 = list(Day.digit_map(day.program[1]))
        maps1 = list(Day.shift_maps(maps1, 3))
        maps = list(Day.merge_maps(maps, maps1))
        maps2 = list(Day.digit_map(day.program[2]))
        maps2 = list(Day.shift_maps(maps2, 6))
        maps = list(Day.merge_maps(maps, maps2))
        for m in maps:
            # print(m)
            v = Day.get_value(m)
            # print(v)
            day.reinit(v)
            day.part1b()

    def show_maps(maps: Iterable[dict[int, int]]) -> None:
        day = Day()
        for m in maps:
            # print(m)
            v = Day.get_value(m)
            # print(v)
            day.reinit(v)
            day.part1b()

    def part2(self) -> None:
        rolling_maps = None
        for i, num in enumerate(self.program):
            print(f"------- {i} -------")
            current_maps = list(Day.digit_map(num))
            if not rolling_maps:
                rolling_maps = current_maps
            else:
                current_maps = list(Day.shift_maps(current_maps, i * 3))
                rolling_maps = list(Day.merge_maps(rolling_maps, current_maps))
            Day.show_maps(rolling_maps)
        values = [Day.get_value(rolling_map) for rolling_map in rolling_maps]
        print(f"Part 2: {min(values)}")


def parts():
    # Day().part1()
    Day().part2()


parts()
