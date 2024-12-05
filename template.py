import io
import sys
from typing import TextIO


def parse_input(input: TextIO) -> ...:
    input.seek(0)
    lines = input.readlines()
    _ = lines


def part1(input: TextIO):
    _ = parse_input(input)


def part2(input: TextIO):
    _ = parse_input(input)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_text = (
            "3   4\n"
            "4   3\n"
            "2   5\n"
            "1   3\n"
            "3   9\n"
            "3   3"
        )

        test_io = io.StringIO(test_text)
        print(f"test part 1: {part1(test_io)}")
        print(f"test part 2: {part2(test_io)}")
        exit(0)

    with open(sys.argv[1]) as file:
        print(f"part 1: {part1(file)}")
        print(f"part 2: {part2(file)}")
