import io
import itertools
import sys
from typing import TextIO


def parse_input(input: TextIO) -> tuple[bytearray, int]:
    input.seek(0)

    lines = [line.rstrip() for line in input]
    assert len(lines) > 0
    width = len(lines[0])

    assert all(len(line) == width for line in lines)
    return bytearray("".join(lines).encode()), width


def print_map(map: bytearray, width: int):
    assert len(map) % width == 0

    for i in range(0, len(map), width):
        print(map[i : i + width].decode())


def antinode_valid(antinode_x: int, antinode_y: int, width: int, height: int) -> bool:
    return (
        antinode_x >= 0
        and antinode_x < width
        and antinode_y >= 0
        and antinode_y < height
    )


def part1(input: TextIO):
    map, width = parse_input(input)
    assert len(map) % width == 0
    height = len(map) // width

    all_antenna_chars = set(map) - {ord(".")}

    antinodes: set[int] = set()
    for antenna_char in all_antenna_chars:
        indices = [map.find(antenna_char)]
        assert indices[0] != -1

        while (index := map.find(antenna_char, indices[-1] + 1)) != -1:
            indices.append(index)

        for a, b in itertools.combinations(indices, 2):
            ax, ay = a % width, a // width
            bx, by = b % width, b // width
            adx, ady = bx - ax, by - ay

            antinode_x, antinode_y = (ax - adx, ay - ady)
            if antinode_valid(antinode_x, antinode_y, width, height):
                antinodes.add(antinode_x + antinode_y * width)

            antinode_x, antinode_y = ax + 2 * adx, ay + 2 * ady
            if antinode_valid(antinode_x, antinode_y, width, height):
                antinodes.add(antinode_x + antinode_y * width)

    map_to_draw = map.copy()
    for antinode in antinodes:
        map_to_draw[antinode] = ord("#")

    print_map(map_to_draw, width)
    return len(antinodes)


def part2(input: TextIO):
    map, width = parse_input(input)
    assert len(map) % width == 0
    height = len(map) // width

    all_antenna_chars = set(map) - {ord(".")}

    antinodes: set[int] = set()
    for antenna_char in all_antenna_chars:
        indices = [map.find(antenna_char)]
        assert indices[0] != -1

        while (index := map.find(antenna_char, indices[-1] + 1)) != -1:
            indices.append(index)

        for a, b in itertools.combinations(indices, 2):
            ax, ay = a % width, a // width
            bx, by = b % width, b // width
            adx, ady = bx - ax, by - ay

            antinode_x, antinode_y = (ax, ay)
            while antinode_valid(antinode_x, antinode_y, width, height):
                antinodes.add(antinode_x + antinode_y * width)
                antinode_x -= adx
                antinode_y -= ady

            antinode_x, antinode_y = (bx, by)
            while antinode_valid(antinode_x, antinode_y, width, height):
                antinodes.add(antinode_x + antinode_y * width)
                antinode_x += adx
                antinode_y += ady

    map_to_draw = map.copy()
    for antinode in antinodes:
        map_to_draw[antinode] = ord("#")

    print_map(map_to_draw, width)
    return len(antinodes)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_text = (
            "............\n"
            "........0...\n"
            ".....0......\n"
            ".......0....\n"
            "....0.......\n"
            "......A.....\n"
            "............\n"
            "............\n"
            "........A...\n"
            ".........A..\n"
            "............\n"
            "............\n"
        )

        test_io = io.StringIO(test_text)
        print(f"test part 1: {part1(test_io)}")
        print(f"test part 2: {part2(test_io)}")
        exit(0)

    with open(sys.argv[1]) as file:
        print(f"part 1: {part1(file)}")
        print(f"part 2: {part2(file)}")
