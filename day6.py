import io
import re
import sys
import colorama
from typing import NamedTuple, TextIO
colorama.init()

ROTATE_MAP = {
    ord("^"): ord(">"),
    ord(">"): ord("v"),
    ord("v"): ord("<"),
    ord("<"): ord("^"),
}

def parse_input(input: TextIO) -> tuple[bytearray, int]:
    input.seek(0)
    lines = [line.strip() for line in input.readlines()]

    assert len(lines) > 0
    map_width = len(lines[0])
    assert all(len(line) == map_width for line in lines)

    return bytearray("".join(lines).encode()), map_width


def print_map(map: bytearray, width: int):
    for i in range(0, len(map), width):
        print(map[i : i + width].decode())

def print_colored_map(map: list[int], width: int):
    for i in range(0, len(map)):
        color = map[i] >> 8
        if color != 0:
            print(f"{colorama.ansi.code_to_chars(color)}{chr(map[i] & 0x7f)}{colorama.Fore.RESET}", end="")
        else:
            print(chr(map[i]), end="")
        if (i + 1) % width == 0:
            print()

def draw_path_on_colored_map(map: list[int], width: int, path: list[int], color: int):
    window: list[int] = []

    for upcoming_index in [*path]:
        if len(window) != 3:
            window.append(upcoming_index)
            continue

        prev_index, index, next_index = window
        if map[index] != ord("."):
            target_char = "+"
        elif index - prev_index == next_index - index:
            abs_diff = abs(next_index - index)
            if abs_diff == 1:
                target_char = "-"
            else:
                target_char = "|"
        else:
            target_char = "+"
        
        map[index] = ord(target_char) + (color << 8)
        window = [index, next_index, upcoming_index]



def print_path(map: bytearray, width: int, *paths: tuple[list[int], int]):
    map_to_print = list(map)

    for path, color in paths:
        draw_path_on_colored_map(map_to_print, width, path, color)

    print_colored_map(map_to_print, width)


GUARD_RE = re.compile(b"[\\^><v]")


def find_guard(map: bytearray) -> int | None:
    match = GUARD_RE.search(map)
    if match is None:
        return None

    return match.start()


def get_step_size(guard_char: int, width: int):
    STEP_MAP = {
        ord("^"): -width,
        ord(">"): 1,
        ord("v"): width,
        ord("<"): -1,
    }
    assert guard_char in STEP_MAP
    return STEP_MAP[guard_char]

def peek_guard(guard_index: int, map: bytearray, width: int) -> int | None:
    step_size = get_step_size(map[guard_index], width)
    next_index = guard_index + step_size

    if next_index >= len(map) or next_index < 0 or (abs(step_size) == 1 and (guard_index // width) != (next_index // width)):
        return
    
    return next_index

def step_guard(guard_index: int, map: bytearray, width: int) -> tuple[int, bool]:
    """
    Move the guard forwards by one step, if possible.

    Returns:
        A tuple of (updated_guard_index, not_at_map_edge). If the input guard index is the 
        same as the returned, and not_at_map_edge is True, then the guard has hit a wall.
    """
    next_index = peek_guard(guard_index, map, width)
    if next_index is None:
        return guard_index, False

    if map[next_index] != ord("."):
        return guard_index,  True
    
    map[next_index], map[guard_index] = map[guard_index], ord(".")
    return next_index, True
    
def rotate_guard(guard_index: int, map: bytearray, width: int):
    for _ in range(3):
        next_char = ROTATE_MAP[map[guard_index]]
        map[guard_index] = next_char
        
        next_index = peek_guard(guard_index, map, width) 
        if next_index is None or map[next_index] == ord("."):
            break
    else:
        raise RuntimeError("Failed to rotate guard! He is stuck :((")


def walk_guard(map: bytearray, width: int, start_index: int | None = None) -> tuple[int, list[int], bool]:
    """Walks the guard to the next wall, or the edge of the map."""

    if start_index is not None:
        guard_index = start_index
    else:
        guard_index = find_guard(map)
        if guard_index is None:
            print("warning: cannot walk guard: no guard can be found")
            return -1, [], False

    indices_walked = [guard_index]

    while True:
        next_index, should_walk = step_guard(guard_index, map, width)
        if should_walk is False:
            return next_index, indices_walked, False
        
        if next_index == guard_index:
            return next_index, indices_walked, True
        
        indices_walked.append(next_index)
        guard_index = next_index


def part1(input: TextIO) -> int:
    map, width = parse_input(input)
    indices_walked: set[int] = set()

    # just assert that we have a guard
    assert find_guard(map) is not None

    while True:
        guard_index, indices, walk_more = walk_guard(map, width)
        print('=' * width)
        print_map(map, width)
        print('=' * width, end="\n\n")

        indices_walked = indices_walked.union(indices)
        if not walk_more:
            break

        rotate_guard(guard_index, map, width)

    print("WALKED AREAS")
    walked_map = map.copy()
    print("=" * width)
    for index in indices_walked:
        walked_map[index] = ord('X')

    print_map(walked_map, width)
    return len(indices_walked)

class UniqueTranslation(NamedTuple):
    position: int
    char_at: int

def find_cycle_if_exist(guard_index: int, map: bytearray, width: int) -> tuple[int, list[int] | None, bytearray]:
    map = map.copy()
    unique_block_hits: set[int] = {guard_index}
    all_steps: list[int] = []

    obstruction_index = peek_guard(guard_index, map, width)
    if obstruction_index is None:
        return -1, None, map

    map[obstruction_index] = ord('O')
    rotate_guard(guard_index, map, width)


    while True:
        guard_index, steps, continue_walking = walk_guard(map, width)
        if not continue_walking:
            return -1, None, map
        
        all_steps.extend(steps)
        if guard_index in unique_block_hits:
            return obstruction_index, all_steps, map

        rotate_guard(guard_index, map, width)
        unique_block_hits.add(guard_index)


def part2(input: TextIO):
    map, width = parse_input(input)
    obstruction_indices: list[int] = []

    # just assert that we have a guard
    guard_index = find_guard(map)
    assert guard_index is not None

    steps: list[int] = []
    while True:
        # have overall set for steps walked before arriving to the test location
        obstruction_index, cycle, cycle_map = find_cycle_if_exist(guard_index, map, width)
        if cycle is not None:
            print('='*width, end="")
            print(f"CYCLE {len(obstruction_indices) + 1}")
            print_path(cycle_map, width, (steps, 31), (cycle, 32))
            if obstruction_index not in steps:
                obstruction_indices.append(obstruction_index)

        steps.append(guard_index)
        next_index, should_walk = step_guard(guard_index, map, width)
        if should_walk is False:
            break
        
        if next_index == guard_index:
            rotate_guard(guard_index, map, width)

        guard_index = next_index

    print(f"Total obstruction placements: {len(obstruction_indices)}")
    return len(set(obstruction_indices))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_text = (
            "....#.....\n"
            ".........#\n"
            "..........\n"
            "..#.......\n"
            ".......#..\n"
            "..........\n"
            ".#..^.....\n"
            "........#.\n"
            "#.........\n"
            "......#..."
        )

        test_io = io.StringIO(test_text)
        print(f"test part 1: {part1(test_io)}")
        print(f"test part 2: {part2(test_io)}")
        exit(0)

    with open(sys.argv[1]) as file:
        print(f"part 1: {part1(file)}")
        print(f"part 2: {part2(file)}")
