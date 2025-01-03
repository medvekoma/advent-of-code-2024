from collections import Counter
from itertools import product
import networkx as nwx
from aoc2024.utils.mynumpy import Matrix
from aoc2024.utils.reader import read_file, read_input


IS_TEST = False
lines = read_input(IS_TEST)


def build_graph_dict(name: str) -> dict[tuple[str, str], list[str]]:
    """For any button pair, return a list of possible optimal paths as a list of directions (^,>,<,v)."""
    pad_lines = read_file(f"{name}.txt")
    matrix = Matrix.from_lines(pad_lines)
    graph: nwx.DiGraph = nwx.DiGraph()
    neighbor_map = {  # is_horz: (r, c)
        True: (0, 1),
        False: (1, 0),
    }
    for pos in matrix.cells():
        this = matrix.get_value(pos)
        if this == " ":
            continue
        for is_horz, offset in neighbor_map.items():
            npos = pos.add(offset)
            that = matrix.get_value(npos)
            if that in [" ", None]:
                continue
            graph.add_edge(this, that, label=(">" if is_horz else "v"))
            graph.add_edge(that, this, label=("<" if is_horz else "^"))
    return {
        (source, target): [
            "".join([graph.get_edge_data(path[i], path[i + 1])["label"] for i in range(len(path) - 1)]) + "A"
            for path in nwx.all_shortest_paths(graph, source, target)
        ]
        for source in graph.nodes
        for target in graph.nodes
    }


numpad_dict = build_graph_dict("numpad")
# keypad_dict = build_graph_dict("keypad")

keypad_dict = {
    ("^", "^"): ["A"],
    ("^", "A"): [">A"],
    ("^", "v"): ["vA"],
    ("^", ">"): ["v>A"],
    ("^", "<"): ["v<A"],
    ("A", "^"): ["<A"],
    ("A", "A"): ["A"],
    ("A", "v"): ["<vA"],
    ("A", ">"): ["vA"],
    ("A", "<"): ["v<<A"],
    ("v", "^"): ["^A"],
    ("v", "A"): ["^>A"],
    ("v", "v"): ["A"],
    ("v", ">"): [">A"],
    ("v", "<"): ["<A"],
    (">", "^"): ["<^A"],
    (">", "A"): ["^A"],
    (">", "v"): ["<A"],
    (">", ">"): ["A"],
    (">", "<"): ["<<A"],
    ("<", "^"): [">^A"],
    ("<", "A"): [">>^A"],
    ("<", "v"): [">A"],
    ("<", ">"): [">>A"],
    ("<", "<"): ["A"],
}


def pad_step(chunk: str, pad_dict: dict[tuple[str, str], list[str]]) -> list[dict[str, int]]:
    chunk = "A" + chunk
    parts = [
        pad_dict[(source, target)]
        for source, target in list(zip(chunk, chunk[1:]))
        #
    ]
    options_list = list(product(*parts))
    return [dict(Counter(option)) for option in options_list]


def numpad_step(chunk: str) -> list[dict[str, int]]:
    return pad_step(chunk, numpad_dict)


def keypad_step(chunk: str) -> list[dict[str, int]]:
    return pad_step(chunk, keypad_dict)


def keypad_iteration(options: list[dict[str, int]]) -> list[dict[str, int]]:
    result = []
    for option in options:
        option_chunks = [
            [
                {k: v * count for k, v in next_chunk.items()}
                for next_chunk in keypad_step(chunk)
                #
            ]
            for chunk, count in option.items()
        ]
        option_combinations = list(product(*option_chunks))
        for option_combination in option_combinations:
            res_dict: dict[str, int] = {}
            for d in option_combination:
                for k, v in d.items():
                    res_dict[k] = res_dict.get(k, 0) + v
            result.append(res_dict)
    result = keep_shortest(result)
    return result


def dict_len(d: dict[str, int]) -> int:
    return sum(len(k) * v for k, v in d.items())


def keep_shortest(options: list[dict[str, int]]) -> list[dict[str, int]]:
    min_len = min(dict_len(opt) for opt in options)
    return [opt for opt in options if dict_len(opt) == min_len]


def calculate_loops(loops: int) -> int:
    result = 0
    for line in lines:
        opts = numpad_step(line)
        for _ in range(loops):
            opts = keypad_iteration(opts)
        result += int(line[0:3]) * dict_len(opts[0])
    return result


def part1() -> None:
    result = calculate_loops(2)
    print(f"Part 1: {result}")


def part2() -> None:
    result = calculate_loops(25)
    print(f"Part 2: {result}")


part1()
part2()
