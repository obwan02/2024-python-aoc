import io
import sys
from contextlib import suppress
from typing import TextIO


def parse_input(input: TextIO) -> ...:
    input.seek(0)
    lines = input.readlines()
    return [line.strip() for line in lines]


def part1(input: TextIO):
    grid = parse_input(input)
    count = 0

    for sy in range(len(grid)):
        for sx in range(len(grid[0])):
            chunk = [line[sx:sx+4] for line in grid[sy:sy+4]]

            horz = chunk[0]
            vert = "".join(line[0] for line in chunk)
            checks = [horz, vert]

            with suppress(IndexError):
                diag1 = "".join(chunk[i  ][i  ] for i in range(4))
                checks.append(diag1)

            with suppress(IndexError):
                diag2 = "".join(chunk[3-i][i  ] for i in range(4))
                checks.append(diag2)

            # print(checks)
            count += sum(1 for line in checks if line == "XMAS" or line == "SAMX")

    return count



def part2(input: TextIO):
    grid = parse_input(input)
    count = 0

    print(len(grid) - 2)
    for sy in range(len(grid) - 2):
        for sx in range(len(grid[0]) - 2):
            diag1 = "".join(grid[sy + i][sx + i] for i in range(3))
            diag2 = "".join(grid[sy + 2 - i][sx + i] for i in range(3))

            print(diag1, diag2, end="")
            if diag1 in ["MAS", "SAM"] and diag2 in ["MAS", "SAM"]:
                count += 1
                print(" YES")
            else:
                print("")

    return count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_text = (
            # "MMMSXXMASM\n"
            # "MSAMXMSMSA\n"
            # "AMXSXMAAMM\n"
            # "MSAMASMSMX\n"
            # "XMASAMXAMM\n"
            # "XXAMMXXAMA\n"
            # "SMSMSASXSS\n"
            # "SAXAMASAAA\n"
            # "MAMMMXMMMM\n"
            # "MXMXAXMASX"
            "M.S\n"
            ".A.\n"
            "M.S"
        )

        test_io = io.StringIO(test_text)
        print(f"test part 1: {part1(test_io)}")
        print(f"test part 2: {part2(test_io)}")
        exit(0)

    with open(sys.argv[1]) as file:
        print(f"part 1: {part1(file)}")
        print(f"part 2: {part2(file)}")
