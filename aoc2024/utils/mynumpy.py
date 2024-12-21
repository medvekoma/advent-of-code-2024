from typing import Any, Callable, Iterable, Optional, TypeVar
import numpy as np

T = TypeVar("T")
type Cell = tuple[int, int]


def identity_string(value: str) -> str:
    return value


class Pos2D(tuple[int, int]):
    def __new__(cls, *args):
        if len(args) == 1 and isinstance(args[0], (tuple, list)) and len(args[0]) == 2:
            return super().__new__(cls, args[0])
        return super().__new__(cls, args)

    def add(self, offset: tuple[int, int]) -> "Pos2D":
        return Pos2D((self[0] + offset[0], self[1] + offset[1]))


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

    def cells(self) -> Iterable[Pos2D]:
        yield from (
            Pos2D(r, c)
            for r in range(self.shape[0])
            for c in range(self.shape[1])
            #
        )

    def has_cell(self, cell: tuple[int, int]) -> bool:
        return 0 <= cell[0] < self.shape[0] and 0 <= cell[1] < self.shape[1]

    def get_value(self, pos: Pos2D) -> Optional[T]:
        return self[pos] if self.has_cell(pos) else None

    def print_chars(self):
        for row in self:
            print("".join(row))

    def findall(self, value: T) -> list[Pos2D]:
        ridx, cidx = np.where(self == value)
        return [Pos2D(r, c) for r, c in zip(ridx, cidx)]
