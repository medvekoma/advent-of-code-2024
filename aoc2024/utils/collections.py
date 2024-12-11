import re
from typing import Callable, TypeVar, Generator, Optional

T = TypeVar("T")


def split_by(the_list: list[T], separator: T) -> Generator[list[T], None, None]:
    start_idx = 0
    for idx, elem in enumerate(the_list):
        if elem == separator:
            yield the_list[start_idx:idx]
            start_idx = idx + 1
    yield the_list[start_idx:]


def split_into(collection: list[T], size: int) -> list[list[T]]:
    return [collection[i : i + size] for i in range(0, len(collection), size)]


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
