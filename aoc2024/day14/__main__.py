from collections import defaultdict
from math import prod
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import parse_ints
from aoc2024.utils.reader import read_lines

IS_TEST = False

lines = read_lines(IS_TEST)

type Cell = tuple[int, int]
type Robot = tuple[Cell, Cell]


class Day14:
    def __init__(self) -> None:
        self.robots = [self.unpack(parse_ints(line)) for line in lines]
        self.shape = (11, 7) if IS_TEST else (101, 103)

    def unpack(self, values: list[int]) -> tuple[Cell, Cell]:
        x, y, vx, vy = values
        return (x, y), (vx, vy)

    def iterations(self, robot: Robot, steps: int) -> Robot:
        (x, y), (vx, vy) = robot
        x = (x + steps * vx) % self.shape[0]
        y = (y + steps * vy) % self.shape[1]
        return (x, y), (vx, vy)

    def compare(self, a, b):
        return (a > b) - (a < b)

    def part1(self) -> None:
        middle = self.shape[0] // 2, self.shape[1] // 2
        robot_counter: dict[Cell, int] = defaultdict(int)
        quadrant_counter: dict[Cell, int] = defaultdict(int)
        for robot in self.robots:
            robot = self.iterations(robot, 100)
            pos = robot[0]
            robot_counter[pos] += 1
            qx = self.compare(pos[0], middle[0])
            qy = self.compare(pos[1], middle[1])
            if qx != 0 and qy != 0:
                quadrant_counter[(qx, qy)] += 1
        result = prod(quadrant_counter.values())
        print(f"Part 1: {result}")


@timer
def parts():
    day = Day14()
    day.part1()


parts()
