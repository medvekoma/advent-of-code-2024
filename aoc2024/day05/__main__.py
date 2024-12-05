from collections import defaultdict
import numpy as np
from aoc2024.utils.collections import parse_lines, split_by
from aoc2024.utils.reader import read_lines

lines = read_lines(is_test=False)


def is_good_list(pages: list[int], rule_dict: dict[int, set[int]]) -> bool:
    for i, page in enumerate(pages):
        if page in rule_dict:
            remaining_pages = pages[i + 1 :]
            preceeding_pages = rule_dict[page]
            if preceeding_pages.intersection(remaining_pages):
                return False
    return True


def part1():
    rules, pages_list = split_by(lines, "")
    rule_list = [(int(a), int(b)) for a, b in parse_lines(rules, r"(\d+)\|(\d+)")]
    rule_dict = defaultdict(set)
    for key, value in rule_list:
        rule_dict[value].add(key)
    rule_dict = dict(rule_dict)
    pages = [[int(page) for page in pages.split(",")] for pages in pages_list]
    good_lists = [page for page in pages if is_good_list(page, rule_dict)]
    middles = [page[len(page) // 2] for page in good_lists]
    return sum(middles)


def part2():
    pass


print(f"part1: {part1()}")
print(f"part2: {part2()}")
