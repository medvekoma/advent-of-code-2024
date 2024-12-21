import networkx as nwx
from aoc2024.utils.mynumpy import Matrix, Pos2D
from aoc2024.utils.reader import read_lines

IS_TEST = False

lines = read_lines(IS_TEST)

type Reindeer = tuple[Pos2D, bool]  # position, is_horizontal


class Day:
    def __init__(self) -> None:
        self.matrix = Matrix.from_lines(lines)
        self.end = self.matrix.findall("E")[0]
        self.start = self.matrix.findall("S")[0]
        self.matrix[self.start] = "."
        self.matrix[self.end] = "."
        self.graph: nwx.Graph = nwx.Graph()
        self.init_graph()

    def init_graph(self) -> None:
        free_cells = self.matrix.findall(".")
        dir_dict = {True: (0, 1), False: (1, 0)}
        for cell in free_cells:
            for is_horz, ncell in dir_dict.items():
                npos = cell.add(ncell)
                if self.matrix.get_value(npos) == ".":
                    self.graph.add_edge((cell, is_horz), (npos, is_horz))
            rotate_weight = 1000 if cell != self.end else 0
            self.graph.add_edge((cell, True), (cell, False), weight=rotate_weight)

    def part1(self) -> None:
        length = nwx.shortest_path_length(self.graph, (self.start, True), (self.end, True), weight="weight")
        print(f"Part 1: {length}")

    def part2(self) -> None:
        paths = nwx.all_shortest_paths(self.graph, (self.start, True), (self.end, True), weight="weight")
        cells = set()
        for path in paths:
            for cell, _ in path:
                cells.add(cell)
        print(f"Part 2: {len(cells)}")


def parts():
    day = Day()
    day.part1()
    day.part2()


parts()
