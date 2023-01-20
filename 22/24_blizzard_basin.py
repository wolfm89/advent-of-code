#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Vec:
    x: int = 0
    y: int = 0

    def __add__(self, other: Vec) -> Vec:
        return Vec(self.x + other.x, self.y + other.y)


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


def read(filename: str) -> tuple[Vec, list[Vec]]:
    with open(filename, "r") as reader:
        next(reader)
        res = []
        for i, line in enumerate(reader):
            res.extend([Blizzard(Vec(i, j - 1), DIR_MAP[c]) for j, c in enumerate(line.strip()) if c in DIR_MAP.keys()])
    return Vec(i - 1, len(line.strip()) - 3), res


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
