from collections import Counter
from aoc2024.utils.reader import read_lines

lines = read_lines()
items = [tuple(map(int, line.strip().split())) for line in lines]
list1, list2 = tuple(zip(*items))


def part1():
    l1 = sorted(list1)
    l2 = sorted(list2)

    diff = [abs(x - y) for x, y in zip(l1, l2)]
    return sum(diff)


def part2():
    counter = Counter(list2)
    occurence_map = {pair[0]: pair[1] for pair in counter.most_common()}
    scores = [x * occurence_map.get(x, 0) for x in list1]
    return sum(scores)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
