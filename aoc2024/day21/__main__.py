from collections import defaultdict
from functools import lru_cache
from itertools import product
from math import prod
from typing import Iterable

import numpy as np
import networkx as nwx
from aoc2024.utils.benchmark import timer
from aoc2024.utils.collections import group_list, parse_ints
from aoc2024.utils.mynumpy import Matrix
from aoc2024.utils.reader import read_input, read_file

IS_TEST = False

lines = read_input(IS_TEST)


class PadGraph:
    def __init__(self, name: str) -> None:
        file_name = f"{name}.txt"
        pad_lines = read_file(file_name)
        self.matrix = Matrix.from_lines(pad_lines)
        self.graph: nwx.DiGraph = nwx.DiGraph()
        self.init_graph()

    def init_graph(self) -> None:
        neighbor_map = {  # is_horz: (r, c)
            True: (0, 1),
            False: (1, 0),
        }
        for pos in self.matrix.cells():
            this = self.matrix.get_value(pos)
            if this == " ":
                continue
            for is_horz, offset in neighbor_map.items():
                npos = pos.add(offset)
                that = self.matrix.get_value(npos)
                if that in [" ", None]:
                    continue
                self.graph.add_edge(this, that, label=">" if is_horz else "v")
                self.graph.add_edge(that, this, label="<" if is_horz else "^")
        self.paths_map = {
            (source, target): self.get_paths(source, target)
            for source in self.graph.nodes
            for target in self.graph.nodes
            #
        }

    def get_paths(self, source: str, target: str) -> list[str]:
        paths = nwx.all_shortest_paths(self.graph, source, target)
        result = []
        for path in paths:
            labels = [self.graph[path[i]][path[i + 1]]["label"] for i in range(len(path) - 1)]
            label_string = "".join(labels) + "A"
            result.append(label_string)
        return result


class Pad:
    def __init__(self, graph: PadGraph) -> None:
        self.graph = graph
        self.cursor = "A"

    def push_buttons(self, sequence: str) -> list[str]:
        label_lists = []
        for button in sequence:
            label_lists.append(self.graph.paths_map[(self.cursor, button)])
            self.cursor = button
        label_sequences = [
            "".join(labels)
            for labels in product(*label_lists)
            #
        ]
        return label_sequences

    def push_buttons_list(self, options: list[str]) -> list[str]:
        options = [
            labels
            for option in options
            for labels in self.push_buttons(option)
            #
        ]
        min_length = len(min(options, key=len))
        shortest_options = [option for option in options if len(option) == min_length]
        return shortest_options


class Day:
    def __init__(self) -> None:
        self.numgraph = PadGraph("numpad")
        self.keygraph = PadGraph("keypad")
        self.numpad = Pad(self.numgraph)
        self.keypad1 = Pad(self.keygraph)
        self.keypad2 = Pad(self.keygraph)
        self.keypad3 = Pad(self.keygraph)

    def get_tripple_press_length(self, source: str, target: str) -> int:
        paths = self.keygraph.get_paths(source, target)
        paths = self.keypad1.push_buttons_list(paths)
        # paths = self.keypad2.push_buttons_list(paths)
        # paths = self.keypad3.push_buttons_list(paths)
        return len(paths[0])

    def part1(self) -> None:
        tripple_path_lengths = {
            (source, target): self.get_tripple_press_length(source, target)
            for source in self.keygraph.graph.nodes
            for target in self.keygraph.graph.nodes
            #
        }

        def get_tripple_length(line: str) -> int:
            line = "A" + line
            result = 0
            for i in range(len(line) - 1):
                source = line[i]
                target = line[i + 1]
                result += tripple_path_lengths[(source, target)]
            return result

        def get_tripple_length2(lines: list[str]) -> int:
            return min(get_tripple_length(line) for line in lines)

        result = 0
        for line in lines:
            paths = self.numpad.push_buttons(line)
            length = get_tripple_length2(paths)
            result += int(line[0:3]) * length
        print(f"Part 1: {result}")


def main():
    day = Day()
    day.part1()


if __name__ == "__main__":
    main()
