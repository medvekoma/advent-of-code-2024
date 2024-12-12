from typing import Any, Callable, Iterable, Optional, TypeVar
import numpy as np

T = TypeVar("T")
type Cell = tuple[int, int]


def identity_string(value: str) -> str:
    return value


class Matrix(np.ndarray):
    def __new__(cls, values: list[list[T]]):
        obj = np.array(values).view(cls)
        return obj

    @staticmethod
    def from_lines(lines: list[str], converter: Callable[[str], Any] = identity_string) -> "Matrix":
        values = [[converter(ch) for ch in line] for line in lines]
        return Matrix(values)

    def neighbors_of(self, cell: tuple[int, int], offsets: Optional[list[Cell]] = None) -> list[Cell]:
        offsets = offsets or [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = [
            (cell[0] + r, cell[1] + c)
            for r, c in offsets
            if 0 <= cell[0] + r < self.shape[0] and 0 <= cell[1] + c < self.shape[1]
        ]
        return neighbors

    def cells(self) -> Iterable[tuple[int, int]]:
        yield from (
            (r, c)
            for r in range(self.shape[0])
            for c in range(self.shape[1])
            #
        )
