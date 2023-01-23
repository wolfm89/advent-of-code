#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Vec:
    x: int = 0
    y: int = 0

    def __add__(self, other: Vec) -> Vec:
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec) -> Vec:
        return Vec(self.x - other.x, self.y - other.y)

    def len(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)


@dataclass
class Blizzard:
    pos: Vec
    dir: Vec


U = Vec(x=-1)
D = Vec(x=1)
L = Vec(y=-1)
R = Vec(y=1)
S = Vec()  # S like stay

DIR_MAP = {">": R, "<": L, "^": U, "v": D}
DIR_MAP_REV = {v: k for k, v in DIR_MAP.items()}

ADJ_POS = [S, U, R, D, L]


def read(filename: str) -> tuple[Vec, list[Blizzard]]:
    with open(filename, "r") as reader:
        next(reader)
        res = []
        for i, line in enumerate(reader):
            res.extend([Blizzard(Vec(i + 1, j), DIR_MAP[c]) for j, c in enumerate(line.strip()) if c in DIR_MAP.keys()])
    return Vec(i, len(line.strip()) - 2), res


def plot(blizzards: list[Blizzard], max_: Vec, positions: list[Vec] = []) -> None:
    entry = 1
    exit = max_.y
    print("".join("#" if i != entry else "." for i in range(max_.y + 2)))
    for i in range(1, max_.x + 1):
        line = "#"
        for j in range(1, max_.y + 1):
            if Vec(i, j) in positions:
                line += "E"
            else:
                blzs = [b for b in blizzards if b.pos == Vec(i, j)]
                line += DIR_MAP_REV[blzs[0].dir] if len(blzs) == 1 else "." if len(blzs) == 0 else f"{len(blzs)}"
        line += "#"
        print(line)
    print("".join("#" if i != exit else "." for i in range(max_.y + 2)))
    print()


def move(blizzards: list[Blizzard], max_: Vec) -> None:
    for blizzard in blizzards:
        blizzard.pos += blizzard.dir
        x_new = p if (p := blizzard.pos.x % max_.x) != 0 else max_.x
        y_new = p if (p := blizzard.pos.y % max_.y) != 0 else max_.y
        blizzard.pos = Vec(x_new, y_new)  # keep in bounds


def is_entry_exit(p: Vec, max_: Vec) -> bool:
    return p == Vec(max_.x + 1, max_.y) or p == Vec(0, 1)


def is_in_bounds(p: Vec, max_: Vec) -> bool:
    return 1 <= p.x <= max_.x and 1 <= p.y <= max_.y


def has_blizzards(p: Vec, blizzards: list[Blizzard]) -> bool:
    return any(p == b.pos for b in blizzards)


def step(E: Vec, blizzards: list[Blizzard], max_: Vec) -> Iterator[Vec]:
    return filter(
        lambda p: (is_entry_exit(p, max_) or is_in_bounds(p, max_)) and not has_blizzards(p, blizzards),
        (E + d for d in ADJ_POS),
    )


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    test: bool = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/24_test.txt")
    else:
        input = read("input/24.txt")

    max_, blizzards = input
    plot(blizzards, max_)

    entry = Vec(0, 1)
    exit = Vec(max_.x + 1, max_.y)
    print(exit)
    t = 0

    positions = [entry]
    while True:
        print(t, len(positions), min(positions, key=lambda p: (exit - p).len()))
        t += 1
        move(blizzards, max_)
        possible_pos = set()
        for pos in positions:
            possible_pos.update(step(pos, blizzards, max_))
        if exit in possible_pos:
            break
        positions = possible_pos
        # plot(blizzards, max_, positions)
    # plot(blizzards, max_, positions)
    print(t)
