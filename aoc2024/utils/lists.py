from typing import Optional


def find_index(lst: list, condition: callable) -> Optional[int]:
    for i, item in enumerate(lst):
        if condition(item):
            return i
    return None


def remove_at(lst: list, index: int) -> list:
    return lst[:index] + lst[index + 1 :]
