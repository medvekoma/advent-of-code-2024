from collections import defaultdict
import math
from itertools import combinations
from aoc2024.utils.reader import read_lines

type Cell = tuple[int, int]

lines = read_lines(is_test=False)
rows = len(lines)
cols = len(lines[0])

antenna_map: dict[str, list[Cell]] = defaultdict(list)

for r, line in enumerate(lines):
    for c, char in enumerate(line):
        if char != ".":
            antenna_map[char].append((r, c))


def is_in_range(cell: Cell) -> bool:
    return 0 <= cell[0] < rows and 0 <= cell[1] < cols


def generate_antidotes(cells: list[Cell]) -> set[Cell]:
    cell_pairs = combinations(cells, 2)
    antidote_pairs = [
        (
            (2 * r1 - r2, 2 * c1 - c2),
            (2 * r2 - r1, 2 * c2 - c1),
        )
        for ((r1, c1), (r2, c2)) in cell_pairs
    ]
    antidotes = {cell for pair in antidote_pairs for cell in pair if is_in_range(cell)}
    return antidotes


def part1():
    all_antidotes = set()
    for cells in antenna_map.values():
        antidotes = generate_antidotes(cells)
        all_antidotes |= antidotes
    return len(all_antidotes)


def get_direction_vector(pair: tuple[Cell, Cell]) -> Cell:
    vector = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])
    # normalize vector
    gcd = math.gcd(*vector)
    return vector[0] // gcd, vector[1] // gcd


def generate_line_antidotes(cell_pair: tuple[Cell, Cell]) -> set[Cell]:
    direction = get_direction_vector(cell_pair)
    antidotes = set()
    cell = cell_pair[0]
    while is_in_range(cell):
        antidotes.add(cell)
        cell = (cell[0] + direction[0], cell[1] + direction[1])
    cell = cell_pair[0]
    while is_in_range(cell):
        antidotes.add(cell)
        cell = (cell[0] - direction[0], cell[1] - direction[1])
    return antidotes


def part2():
    all_antidotes = set()
    for cells in antenna_map.values():
        pairs = combinations(cells, 2)
        for pair in pairs:
            antidotes = generate_line_antidotes(pair)
            all_antidotes |= antidotes
    return len(all_antidotes)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
