def read_text(path: str = "input.txt") -> str:
    with open(path, "r") as file:
        return file.read().strip()


def read_lines(path: str = "input.txt") -> list[str]:
    with open(path, "r") as file:
        return file.readlines()
