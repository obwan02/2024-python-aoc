import io
import sys
from typing import TextIO

def sign(x: int):
    if x == 0:
        return 0
    return x // abs(x)


def is_safe(record):
    seq_diffs = [a - b for a, b in zip(record[:-1], record[1:])]
    diff_sign = sign(seq_diffs[0])
    return all(abs(diff) <= 3 and abs(diff) >= 1 and sign(diff) == diff_sign for diff in seq_diffs)


def parse_input(input: TextIO) -> ...:
    input.seek(0)
    lines = input.readlines()
    return [list(map(int, line.split())) for line in lines]


def part1(input: TextIO):
    records = parse_input(input)
    num_safe_records = 0

    for record in records:
        safe = is_safe(record)
        num_safe_records += 1 if safe else 0

    return num_safe_records


def part2(input: TextIO):
    records = parse_input(input)
    num_safe_records = 0

    for record in records:
        safe = any(is_safe(record[:i] + record[i+1:]) for i in range(len(record)))
        num_safe_records += 1 if safe else 0

    return num_safe_records


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_text = (
            "7 6 4 2 1\n"
            "1 2 7 8 9\n"
            "9 7 6 2 1\n"
            "1 3 2 4 5\n"
            "8 6 4 4 1\n"
            "1 3 6 7 9\n"
        )

        test_io = io.StringIO(test_text)
        print(f"test part 1: {part1(test_io)}")
        print(f"test part 2: {part2(test_io)}")
        exit(0)

    with open(sys.argv[1]) as file:
        print(f"part 1: {part1(file)}")
        print(f"part 2: {part2(file)}")
