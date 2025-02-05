import re
from typing import Callable, Iterable, TypeVar, Generator, Optional

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def split_by_func(the_list: list[T], condition: Callable[[T], bool]) -> Iterable[list[T]]:
    start_idx = 0
    for idx, elem in enumerate(the_list):
        if condition(elem):
            yield the_list[start_idx:idx]
            start_idx = idx + 1
    yield the_list[start_idx:]


def split_by(the_list: list[T], separator: T) -> Iterable[list[T]]:
    return split_by_func(the_list, lambda x: x == separator)


def partition(collection: list[T], condition: Callable[[T], bool]) -> tuple[list[T], list[T]]:
    result: dict[bool, list[T]] = {True: [], False: []}
    for item in collection:
        result[condition(item)].append(item)
    return result[True], result[False]


def find_index(lst: list, condition: Callable) -> Optional[int]:
    for i, item in enumerate(lst):
        if condition(item):
            return i
    return None


def remove_at(lst: list, index: int) -> list:
    return lst[:index] + lst[index + 1 :]


def parse_lines(lines: list[str], pattern: str) -> list[tuple]:
    matches = [re.search(pattern, line) for line in lines]
    return [match.groups() for match in matches if match]


def parse_ints(line: str) -> list[int]:
    return [int(s) for s in re.findall(r"\-?\d+", line)]


def identity(x):
    return x


def group_list(
    lst: list[T],
    key: Callable[[T], K] = identity,
    value: Callable[[T], V] = identity,
) -> dict[K, list[V]]:
    result: dict[K, list[V]] = {}
    for item in lst:
        k = key(item)
        v = value(item)
        if k not in result:
            result[k] = []
        result[k].append(v)
    return result
