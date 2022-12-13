#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import defaultdict
import re
import copy


def read_stacks(filename):
    stacks = defaultdict(list)
    with open(filename, "r") as reader:
        line = reader.readline()
        while "[" in line:
            crates = [c for i, c in enumerate(line) if ((i - 1) % 4) == 0]
            for i, c in enumerate(crates):
                if c != " ":
                    stacks[i + 1].append(c)
            line = reader.readline()
    for k in stacks.keys():
        stacks[k] = list(reversed(stacks[k]))
    return stacks


def read_instructions(filename):
    with open(filename, "r") as reader:
        line = reader.readline()
        while line != "\n":
            line = reader.readline()
        line = reader.readline()
        instructions = []
        while line.startswith("move"):
            instruction = [int(c) for c in re.findall(r"\d+", line)]
            instructions.append(instruction)
            line = reader.readline()
    return instructions


def uppermost_crates(stacks):
    uppermost_crates = ""
    for s in sorted(stacks.keys()):
        uppermost_crates += stacks[s][-1]
    return uppermost_crates


def move(instruction, stacks, rev=True):
    quantity, origin, destination = instruction
    if rev:
        stacks[destination].extend(reversed(stacks[origin][-quantity:]))
    else:
        stacks[destination].extend(stacks[origin][-quantity:])
    del stacks[origin][-quantity:]


if __name__ == "__main__":
    stacks9000 = read_stacks("input/5.txt")
    stacks9001 = copy.deepcopy(stacks9000)
    instructions = read_instructions("input/5.txt")

    print(uppermost_crates(stacks9000))

    for instruction in instructions:
        move(instruction, stacks9000)

    print(uppermost_crates(stacks9000))

    for instruction in instructions:
        move(instruction, stacks9001, rev=False)

    print(uppermost_crates(stacks9001))
