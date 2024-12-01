from infixpy import *
from collections import Counter

from advent_of_code_2024.utils.reader import read_lines

lines = read_lines()
items = (
    Seq(lines)
    .map(lambda s: s.strip().split())
    .map(lambda s: (int(s[0]), int(s[1])))
    .tolist()
)


def part1():
    l1, l2 = tuple(zip(*items))
    l1 = sorted(l1)
    l2 = sorted(l2)

    diff = [abs(x - y) for x, y in zip(l1, l2)]
    return sum(diff)


def part2():
    list1, list2 = list(zip(*items))
    counter = Counter(list2)
    occurence_map = {pair[0]: pair[1] for pair in counter.most_common()}
    scores = [x * occurence_map.get(x, 0) for x in list1]
    return sum(scores)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
