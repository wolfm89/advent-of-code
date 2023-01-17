#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Vec:
    x: float = 0
    y: float = 0

    def __add__(self, other: Vec) -> Vec:
        return Vec(self.x + other.x, self.y + other.y, self.z + other.z)


S = Vec(x=1)
E = Vec(y=1)
N = Vec(x=-1)
W = Vec(y=-1)


def read(filename: str) -> None:
    with open(filename, "r") as reader:
        res = []
        for i, line in enumerate(reader):
            res.extend([Vec(i, j) for j, c in enumerate(line) if c == "#"])
    return res


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    test: bool = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/23_test.txt")
    else:
        input = read("input/23.txt")

    elves = input

    print(elves)
