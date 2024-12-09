import io
import sys
from typing import TextIO


def parse_input(input: TextIO) -> tuple[dict[int, list[int]], list[list[int]]]:
    input.seek(0)
    rules = {}
    rev_rules = {}
    updates = []
    
    while (line := input.readline()) != "\n":
        line = line.strip()
        before, bar, after = line.partition("|")
        assert bar == "|"

        before_int, after_int = int(before), int(after)
        if after_int not in rules:
            rules[after_int] = []
        if before_int not in rev_rules:
            rev_rules[before_int] = []

        rules[after_int].append(before_int)
        rev_rules[before_int].append(after_int)

    while (line := input.readline()):
        updates.append([int(x) for x in line.split(",")])

    return rules, rev_rules, updates


def check_violations(update: list[int], rules: dict[int, list[int]]) -> list[int]:
    ...


def part1(input: TextIO):
    rules, _, updates = parse_input(input)

    # we have rules such as
    # 97 must come before 75
    #
    # t.f. we run through the input list
    # If we see 75 then we ensure we don't see
    # 97 anywhere in the list
    total = 0

    for update in updates:
        cannot_see = set()
        for page in update:
            if page in cannot_see:
                break

            if page not in rules:
                continue

            cannot_see.update(rules[page])
        else:
            middle = update[len(update) // 2]
            total += middle

    return total


def part2(input: TextIO):
    _ = parse_input(input)
    rules, rev_rules, updates = parse_input(input)

    # how to find correct ordering?
    # 1. we need to find violations
    # 2. 
    #   we should then figure out if *directly* fixing these
    #   violations will break our rules
    # 3. if so, we need to change the order in which fixes are applied ...
    # 
    # -- how to order the fixes correctly --
    # we know:
    # - all fixes should move items backwards in a list
    # - moving an item backwards may violate other rules involving the moved item
    #   - if we *directly* fix the violation, we should *never* be breaking any other rules,
    #     otherwise the update we have is malformed (can never be correct)
    #   - t.f. the only thing we have to care about is the order / placement of corrections


    total = 0

    for update in updates:
        cannot_see = set()
        violations = []

        for page in update:
            if page in cannot_see:
                violations.append(page)

            if page not in rules:
                continue

            cannot_see.update(rules[page])

        if len(violations) > 0:
            new_update = update.copy()

            for violated in violations:
                befores = rev_rules[violated]
                earliest_index = min(update.index(before) for before in befores if before in update)
                old_index = update.index(violated)
                assert earliest_index < old_index

                new_update[old_index], new_update[earliest_index] = new_update[earliest_index], new_update[old_index]
            
            print(new_update, f"(mv {violations})")
        else:
            print(update)

    return total


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_text = (
            "47|53\n"
            "97|13\n"
            "97|61\n"
            "97|47\n"
            "75|29\n"
            "61|13\n"
            "75|53\n"
            "29|13\n"
            "97|29\n"
            "53|29\n"
            "61|53\n"
            "97|53\n"
            "61|29\n"
            "47|13\n"
            "75|47\n"
            "97|75\n"
            "47|61\n"
            "75|61\n"
            "47|29\n"
            "75|13\n"
            "53|13\n"
            "\n"
            "75,47,61,53,29\n"
            "97,61,53,29,13\n"
            "75,29,13\n"
            "75,97,47,61,53\n"
            "61,13,29\n"
            "97,13,75,29,47\n"
        )

        test_io = io.StringIO(test_text)
        print(f"test part 1: {part1(test_io)}")
        print(f"test part 2: {part2(test_io)}")
        exit(0)

    with open(sys.argv[1]) as file:
        print(f"part 1: {part1(file)}")
        print(f"part 2: {part2(file)}")
