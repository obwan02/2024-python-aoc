import io
import itertools
import sys
from typing import TextIO


def parse_input(input: TextIO) -> list[tuple[int, tuple[int, ...]]]:
    input.seek(0)
    splits = (line.split(":", 1) for line in input)
    return [
        (int(total), tuple(int(x) for x in numbers.strip().split()))
        for total, numbers in splits
    ]


def evaluate_expression(numbers: tuple[int, ...], operators: tuple[str, ...]) -> int:
    assert len(operators) == len(numbers) - 1
    assert len(numbers) > 0

    total = numbers[0]
    for number, operator in zip(numbers[1:], operators):
        if operator == "||":
            total = int(f"{total}{number}")
        elif operator == "+":
            total += number
        else:
            total *= number
        # else:
        #     expression = f"total {operator} {number}"
        #     total = eval(expression, {}, {"total": total})

    return total


def search_operator_combinations(
    total: int,
    numbers: tuple[int, ...],
    all_operators: tuple[str, ...] = ("+", "*"),
) -> int:
    assert len(numbers) >= 2

    num_matches = 0
    for operators in itertools.product(all_operators, repeat=len(numbers) - 1):
        # convert to binary number then
        # map each digit to an operator
        evaluation = evaluate_expression(numbers, operators)
        if evaluation == total:
            print(
                "numbers",
                numbers,
                "operators",
                operators,
                "=",
                evaluation,
                "want",
                total,
            )
            num_matches += 1

    return num_matches


def part1(input: TextIO):
    entries = parse_input(input)
    return sum(
        total
        for total, numbers in entries
        if search_operator_combinations(total, numbers) > 0
    )


def part2(input: TextIO):
    entries = parse_input(input)
    return sum(
        total
        for total, numbers in entries
        if search_operator_combinations(total, numbers, ("+", "*", "||")) > 0
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_text = (
            "190: 10 19\n"
            "3267: 81 40 27\n"
            "83: 17 5\n"
            "156: 15 6\n"
            "7290: 6 8 6 15\n"
            "161011: 16 10 13\n"
            "192: 17 8 14\n"
            "21037: 9 7 18 13\n"
            "292: 11 6 16 20"
        )

        test_io = io.StringIO(test_text)
        print(f"test part 1: {part1(test_io)}")
        print(f"test part 2: {part2(test_io)}")
        exit(0)

    with open(sys.argv[1]) as file:
        print(f"part 1: {part1(file)}")
        print(f"part 2: {part2(file)}")
