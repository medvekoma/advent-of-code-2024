import re
from aoc2024.utils.reader import read_lines


lines = read_lines(is_test=False)
content: str = "".join(lines)


def part1():
    matches = re.findall(r"mul\((\d+),(\d+)\)", content)
    matches = [(int(a), int(b)) for a, b in matches]
    return sum(a * b for a, b in matches)


def part2():
    text2 = "do()" + content + "don't()"
    matches = re.findall(r"do\(\)(.+?)don't\(\)", text2)
    all_text = "".join(matches)
    matches = re.findall(r"mul\((\d+),(\d+)\)", all_text)
    matches = [(int(a), int(b)) for a, b in matches]
    return sum(a * b for a, b in matches)


print(f"part1: {part1()}")
print(f"part2: {part2()}")
