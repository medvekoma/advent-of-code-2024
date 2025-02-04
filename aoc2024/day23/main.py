import networkx as nwx
from aoc2024.utils.benchmark import timer
from aoc2024.utils.reader import read_input


IS_TEST = False
lines = read_input(IS_TEST)


def create_graph() -> nwx.Graph:
    graph: nwx.Graph = nwx.Graph()
    for line in lines:
        node1, node2 = line.split("-")
        graph.add_edge(node1, node2)
    return graph


def find_cycles(graph: nwx.Graph) -> list[list[str]]:
    cycles = nwx.simple_cycles(graph, length_bound=3)
    good_cycles = [
        cycle
        for cycle in cycles
        if any(node.startswith("t") for node in cycle)
        #
    ]
    return good_cycles


@timer
def parts() -> None:
    graph = create_graph()
    cycles = find_cycles(graph)
    print(f"Part1: {len(cycles)}")
    cliques = nwx.find_cliques(graph)
    largest_clique = max(cliques, key=len)
    password = ",".join(sorted(largest_clique))
    print(f"Part2: {password}")


if __name__ == "__main__":
    parts()
