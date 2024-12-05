import re
import io
import sys
from typing import TextIO


def part1(input: TextIO):
    text = input.read()

    total = 0
    mul_re = re.compile(r"mul\((\d+),(\d+)\)")
    for item in mul_re.finditer(text):
        a, b = item.group(1), item.group(2)
        a, b = int(a), int(b)
        total += a * b

    return total


def part2(input: TextIO):
    input.seek(0)
    text = input.read()

    total = 0
    mul_re = re.compile(r"(mul|don't|do)\((?:(\d+),(\d+))?\)")
    enabled = True

    for item in mul_re.finditer(text):
        cmd = item.group(1)
        print(cmd)
        if cmd == "don't":
            enabled = False
            continue
        if cmd == "do":
            enabled = True
            continue

        assert cmd == "mul"
        if not enabled:
            continue

        a, b = item.group(2), item.group(3)
        a, b = int(a), int(b)
        total += a * b

    return total


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_text = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

        test_io = io.StringIO(test_text)
        print(f"test part 1: {part1(test_io)}")
        print(f"test part 2: {part2(test_io)}")
        exit(0)

    with open(sys.argv[1]) as file:
        print(f"part 1: {part1(file)}")
        print(f"part 2: {part2(file)}")
