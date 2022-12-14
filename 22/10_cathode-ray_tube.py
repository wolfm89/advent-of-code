#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class Instr(Enum):
    NOOP = 1
    ADDX = 2


def read(filename):
    instructions = []
    with open(filename, "r") as reader:
        for line in reader:
            if line.strip().startswith("noop"):
                instructions.append((Instr.NOOP,))
            else:
                instructions.append((Instr.ADDX, int(line.strip().split(" ")[1])))
    return instructions


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def draw(X_history):
    for row in chunks(X_history, 40):
        l = ""
        for i, X in enumerate(row):
            if X - 1 <= i <= X + 1:
                l += "#"
            else:
                l += "."
        print(l)


def play(instructions):
    X = 1
    X_history = [X]
    for instruction in instructions:
        if instruction[0] == Instr.NOOP:
            X_history.append(X)
        elif instruction[0] == Instr.ADDX:
            X_history.append(X)
            X += instruction[1]
            X_history.append(X)
    return X_history[:-1]

if __name__ == "__main__":
    instructions = read("input/10.txt")
    X_history = play(instructions)

    print(sum(X_history[i] * (i + 1) for i in range(20 - 1, 220, 40)))

    draw(X_history)
