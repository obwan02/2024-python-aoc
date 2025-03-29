import io
import math
import sys
from typing import TextIO

SPACE = -1


def parse_input(input: TextIO) -> str:
    input.seek(0)
    return input.readline().strip()


def expand_fs(compressed: str) -> list[int]:
    in_file = True
    current_id = 0
    result: list[int] = []

    for size in compressed:
        if in_file:
            result.extend([current_id] * int(size))
            current_id += 1
        else:
            result.extend([SPACE] * int(size))

        in_file = not in_file

    return result


def format_uncompressed(data: list[int]) -> str:
    return "".join("." if x == SPACE else str(x) for x in data)


def calculate_checksum(data: list[int]) -> int:
    return sum(index * item for index, item in enumerate(data) if item != SPACE)


def squash_fs_fragmented(data: list[int]):
    write_ptr = 0
    read_ptr = len(data) - 1

    # perform swaps
    for _ in range(len(data) + 1):
        while data[write_ptr] != SPACE:
            write_ptr += 1

        while data[read_ptr] == SPACE:
            read_ptr -= 1

        if read_ptr <= write_ptr:
            break

        # debug printing for pointers - only works
        # for the test case where each file has a single digit ID.
        #
        # ptr_str = "".join(
        #     "^" if i == write_ptr or i == read_ptr else "_" for i in range(len(data))
        # )
        # print("STATE:", format_uncompressed(data))
        # print("PTRS :", ptr_str)
        assert data[write_ptr] == SPACE
        assert data[read_ptr] != SPACE

        data[write_ptr], data[read_ptr] = data[read_ptr], SPACE
        write_ptr += 1
        read_ptr -= 1
    else:
        assert False, "failed to complete operation in maximum time bound"


def part1(input: TextIO):
    compressed_fs = parse_input(input)
    uncompressed = expand_fs(compressed_fs)

    print("UNCOMPRESSED: ", format_uncompressed(uncompressed))
    squash_fs_fragmented(uncompressed)
    print("SOLVED:", format_uncompressed(uncompressed))
    return calculate_checksum(uncompressed)


def find_file_ltr(file_id: int, data: list[int], /, start: int = 0) -> tuple[int, int]:
    block_index = -1
    file_size = 0
    for i in range(start, len(data)):
        if data[i] == file_id:
            if file_size == 0:
                block_index = i
                file_size = 1
            else:
                file_size += 1

        if file_size != 0 and data[i] != file_id:
            return block_index, file_size

    return -1, 0


def print_state_and_ptr(ptr: int, data: list[int]):
    ptr_str = "".join("^" if i == ptr else "_" for i in range(len(data)))
    print("STATE:", format_uncompressed(data))
    print("PTRS :", ptr_str)


def squash_fs_blocked(data: list[int]):
    read_ptr = len(data) - 1
    last_file_id = math.inf

    # TODO: a faster method would be to categorise all the empty
    # spaces beforehand, and then as the block are moved update the list of
    # spaces. This avoids having to re-search from empty blocks from the
    # start.

    while read_ptr >= 0:
        while data[read_ptr] == SPACE:
            read_ptr -= 1

        file_id = data[read_ptr]
        file_size = 1
        while data[read_ptr - 1] == file_id:
            file_size += 1
            read_ptr -= 1

        # if we encounter a block that has a higher
        # file ID then the one we are currently working
        # on, then we can skip as is must've already been
        # moved.
        # assert last_file_id != file_id
        if file_id > last_file_id:
            read_ptr -= 1
            continue

        last_file_id = file_id
        space_ptr, space_size = find_file_ltr(SPACE, data, 0)
        while space_ptr != -1 and space_ptr < read_ptr and space_size < file_size:
            space_ptr, space_size = find_file_ltr(
                SPACE,
                data,
                start=space_ptr + space_size,
            )

        if space_size < file_size or space_ptr >= read_ptr:
            read_ptr -= 1
            continue

        assert space_size > 0
        # print_state_and_ptr(read_ptr, data)
        file_data = data[read_ptr : read_ptr + file_size]
        data[space_ptr : space_ptr + space_size] = file_data + [SPACE] * (
            space_size - file_size
        )
        data[read_ptr : read_ptr + file_size] = [SPACE] * file_size
        # print_state_and_ptr(read_ptr, data)


def part2(input: TextIO):
    compressed_fs = parse_input(input)
    uncompressed = expand_fs(compressed_fs)

    print("UNCOMPRESSED: ", format_uncompressed(uncompressed))
    squash_fs_blocked(uncompressed)
    print("SOLVED:", format_uncompressed(uncompressed))
    return calculate_checksum(uncompressed)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_text = "2333133121414131402"
        test_io = io.StringIO(test_text)
        print(f"test part 1: {part1(test_io)}")
        print(f"test part 2: {part2(test_io)}")
        exit(0)

    with open(sys.argv[1]) as file:
        print(f"part 1: {part1(file)}")
        print(f"part 2: {part2(file)}")
