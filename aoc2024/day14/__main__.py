from collections import defaultdict
from math import prod
from typing import Iterable

import numpy as np
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import group_list, parse_ints
from aoc2024.utils.reader import read_lines

IS_TEST = False

lines = read_lines(IS_TEST)

type Cell = tuple[int, int]
type Robot = tuple[Cell, Cell]


class Day14:
    def __init__(self) -> None:
        values = [parse_ints(line) for line in lines]
        self.robot_dict = group_list(values, key=lambda v: (v[0], v[1]), value=lambda v: (v[2], v[3]))
        self.shape = (11, 7) if IS_TEST else (101, 103)
        self.middle = self.shape[0] // 2, self.shape[1] // 2

    def move_robot(self, pos: Cell, velo: Cell, steps: int) -> tuple[Cell, Cell]:
        (x, y), (vx, vy) = pos, velo
        x = (x + steps * vx) % self.shape[0]
        y = (y + steps * vy) % self.shape[1]
        return (x, y), (vx, vy)

    def move_robots(self, robot_dict: dict[Cell, list[Cell]], steps: int) -> dict[Cell, list[Cell]]:
        new_robot_dict: dict[Cell, list[Cell]] = defaultdict(list)
        for pos, velocities in robot_dict.items():
            for velo in velocities:
                npos, nvelo = self.move_robot(pos, velo, steps)
                new_robot_dict[npos].append(nvelo)
        return new_robot_dict

    def draw_robots(self, positions: Iterable[Cell]) -> None:
        space = np.full((self.shape[1], self.shape[0]), " ", dtype=str)
        for x, y in positions:
            space[y, x] = "#"
        for row in space:
            print("".join(row))

    def is_tree(self, robot_dict: dict[Cell, list[Cell]]) -> bool:
        cells = robot_dict.keys()
        for row in range(self.shape[1]):
            xlist = [x for x, y in cells if y == row]
            if xlist:
                xlist.sort()
                rlist = list(reversed(xlist))
                diffs = {r - l for l, r in zip(xlist, rlist)}
                if max(diffs) > 3:
                    return False
        return True

    def compare(self, a, b):
        return (a > b) - (a < b)

    def part1(self) -> None:
        robot_dict = self.move_robots(self.robot_dict, 100)
        qd: dict[Cell, int] = defaultdict(int)
        for (x, y), velocities in robot_dict.items():
            qx = self.compare(x, self.middle[0])
            qy = self.compare(y, self.middle[1])
            if qx != 0 and qy != 0:
                qd[(qx, qy)] += len(velocities)
        result = prod(qd.values())
        print(f"Part 1: {result}")

    def part2(self) -> None:
        robot_dict = self.robot_dict
        steps = 0
        while not self.is_tree(robot_dict):
            robot_dict = self.move_robots(robot_dict, steps=1)
            print(f"Step {steps}")
            steps += 1

        self.draw_robots(robot_dict.keys())
        print(f"Part 2: {steps}")


@timer
def parts():
    day = Day14()
    day.part1()


parts()
