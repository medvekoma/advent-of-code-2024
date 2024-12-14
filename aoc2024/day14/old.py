from collections import defaultdict
from math import prod
from typing import Iterable

import numpy as np
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import parse_ints
from aoc2024.utils.reader import read_lines

IS_TEST = True

lines = read_lines(IS_TEST)

type Cell = tuple[int, int]
type Robot = tuple[Cell, Cell]


class Day14:
    def __init__(self) -> None:
        self.robots = [self.unpack(parse_ints(line)) for line in lines]
        self.shape = (11, 7) if IS_TEST else (101, 103)
        self.middle = self.shape[0] // 2, self.shape[1] // 2

    def unpack(self, values: list[int]) -> tuple[Cell, Cell]:
        x, y, vx, vy = values
        return (x, y), (vx, vy)

    def move_robot(self, robot: Robot, steps: int) -> Robot:
        (x, y), (vx, vy) = robot
        x = (x + steps * vx) % self.shape[0]
        y = (y + steps * vy) % self.shape[1]
        return (x, y), (vx, vy)

    def compare(self, a, b):
        return (a > b) - (a < b)

    def part1(self) -> None:
        robot_counter: dict[Cell, int] = defaultdict(int)
        quadrant_counter: dict[Cell, int] = defaultdict(int)
        for robot in self.robots:
            robot = self.move_robot(robot, 100)
            pos = robot[0]
            robot_counter[pos] += 1
            qx = self.compare(pos[0], self.middle[0])
            qy = self.compare(pos[1], self.middle[1])
            if qx != 0 and qy != 0:
                quadrant_counter[(qx, qy)] += 1
        result = prod(quadrant_counter.values())
        print(f"Part 1: {result}")

    def draw_robots(self, positions: Iterable[Cell]) -> None:
        space = np.full((self.shape[1], self.shape[0]), " ", dtype=str)
        for x, y in positions:
            space[y, x] = "#"
        print(space)

    def is_symmetric(self, positions: Iterable[Cell]) -> bool:
        pos_list = list(positions)
        for x, y in pos_list:
            offset_y = self.shape[1] - 1 - y
            if (x, offset_y) not in pos_list:
                return False
        return True

    def move_robots(self, robot_dict: dict[Cell, list[Cell]]) -> dict[Cell, list[Cell]]:
        new_robot_dict: dict[Cell, list[Cell]] = defaultdict(list)
        for (x, y), velocities in robot_dict.items():
            for vx, vy in velocities:
                new_pos = ((x + vx) % self.shape[0], (y + vy) % self.shape[1])
                new_robot_dict[new_pos].append((vx, vy))
        return new_robot_dict

    def part2(self) -> None:
        robot_dict: dict[Cell, list[Cell]] = defaultdict(list)
        for pos, velo in self.robots:
            robot_dict[pos].append(velo)
        self.draw_robots(robot_dict.keys())
        steps = 0
        while True:
            robot_dict = self.move_robots(robot_dict)
            steps += 1
            if self.is_symmetric(robot_dict.keys()):
                break
        self.draw_robots(robot_dict.keys())
        print(f"Part 2: {steps}")


@timer
def parts():
    day = Day14()
    day.part2()


parts()
