from collections import defaultdict
from aoc2024.utils.collections import parse_lines, partition, split_by
from aoc2024.utils.reader import read_lines

lines = read_lines(is_test=False)


def is_good_list(pages: list[int], reverse_rule_dict: dict[int, set[int]]) -> bool:
    for i, page in enumerate(pages):
        if page in reverse_rule_dict:
            remaining_pages = pages[i + 1 :]
            preceeding_pages = reverse_rule_dict[page]
            if preceeding_pages.intersection(remaining_pages):
                return False
    return True


rule_lines, pages_lines = split_by(lines, "")
rule_list = [(int(a), int(b)) for a, b in parse_lines(rule_lines, r"(\d+)\|(\d+)")]
reversed_rules = defaultdict(set)
for key, value in rule_list:
    reversed_rules[value].add(key)
pages_list = [[int(page) for page in pages.split(",")] for pages in pages_lines]
good_lists, bad_lists = partition(pages_list, lambda pages: is_good_list(pages, reversed_rules))


def part1():
    middles = [page[len(page) // 2] for page in good_lists]
    return sum(middles)


def fix_pages(pages: list[int], reverse_rule_dict: dict[int, set[int]]) -> list[int]:
    for i, page in enumerate(pages):
        preceeding_pages = reverse_rule_dict.get(page, set())
        if preceeding_pages:
            remaining_pages = pages[i + 1 :]
            first_bad_page = next((item for item in remaining_pages if item in preceeding_pages), None)
            if first_bad_page:
                fixed_pages = pages[:i] + [first_bad_page, page] + [p for p in pages[i + 1 :] if p != first_bad_page]
                return fix_pages(fixed_pages, reverse_rule_dict)
    return pages


def part2():
    fixed_pages = [fix_pages(pages, reversed_rules) for pages in bad_lists]
    middles = [page[len(page) // 2] for page in fixed_pages]
    return sum(middles)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
