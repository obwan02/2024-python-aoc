import io
import sys
import textwrap
from typing import TextIO

def parse_input(input: TextIO) -> tuple[list[int], list[int]]:
    input.seek(0)
    lines = input.readlines()
    left_strs, right_strs = zip(*[line.split() for line in lines])
    left = list(sorted(map(int, left_strs)))
    right = list(sorted(map(int, right_strs)))

    return left, right

def part1(input: TextIO):
    left, right = parse_input(input)
    diff_sum = sum(abs(x - y) for x, y in zip(left, right))
    return diff_sum

def part2(input: TextIO):
    left, right = parse_input(input)
    count_map = {}
    for item in right:
        count_map[item] = count_map.get(item, 0) + 1

    return sum(item * count_map.get(item, 0) for item in left)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_text = ("3   4\n"
                     "4   3\n"
                     "2   5\n"
                     "1   3\n"
                     "3   9\n"
                     "3   3")

        test_io = io.StringIO(test_text)
        print(f"test part 1: {part1(test_io)}")
        print(f"test part 2: {part2(test_io)}")
        exit(0)

    with open(sys.argv[1]) as file:
        print(f"part 1: {part1(file)}")
        print(f"part 2: {part2(file)}")
