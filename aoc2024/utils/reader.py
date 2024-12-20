import inspect
from os import path


def read_lines(is_test: bool = False) -> list[str]:
    file_name = "input_test.txt" if is_test else "input_real.txt"
    file_path = path.join(path.dirname((inspect.stack()[1])[1]), file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.rstrip() for line in file]


def read_text(is_test: bool = False) -> str:
    file_name = "input_test.txt" if is_test else "input_real.txt"
    file_path = path.join(path.dirname((inspect.stack()[1])[1]), file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
