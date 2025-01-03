from aoc2024.utils.benchmark import timer
from aoc2024.utils.reader import read_input


IS_TEST = False
lines = read_input(IS_TEST)


def mix_prune(number: int, secret: int) -> int:
    return (number & 0xFFFFFF) ^ secret


def step(secret: int) -> int:
    secret = mix_prune(secret << 6, secret)
    secret = mix_prune(secret >> 5, secret)
    secret = mix_prune(secret << 11, secret)
    return secret


def steps(secret: int, count: int) -> int:
    for _ in range(count):
        secret = step(secret)
    return secret


@timer
def part1() -> None:
    secrets = [steps(int(line), 2000) for line in lines]
    result = sum(secrets)
    print(f"Part1: {result}")


def part2() -> None:
    secret = 123
    for _ in range(2000):
        secret = step(secret)
        print(f"{secret % 10},", end="")
    print()


if __name__ == "__main__":
    part1()
    # part2()
