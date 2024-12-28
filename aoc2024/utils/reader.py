import inspect
from os import path


def read_input(is_test: bool = False) -> list[str]:
    file_name = "input_test.txt" if is_test else "input_real.txt"
    file_path = path.join(path.dirname((inspect.stack()[1])[1]), file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.rstrip() for line in file]


def read_file(file_name: str) -> list[str]:
    file_path = path.join(path.dirname((inspect.stack()[1])[1]), file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.rstrip() for line in file]
