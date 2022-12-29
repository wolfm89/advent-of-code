#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import NamedTuple
from itertools import product


class Pos(NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0


class Cube(NamedTuple):
    pos: Pos

    @property
    def sides2(self):
        ss = [
            [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1]],
            [[0, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 1]],
            [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]],
            [[1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]],
            [[0, 1, 0], [0, 1, 1], [1, 1, 0], [1, 1, 1]],
            [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]],
        ]
        for i, j in product(range(len(ss)), range(len(ss[0]))):
            ss[i][j][0] += self.pos.x
            ss[i][j][1] += self.pos.y
            ss[i][j][2] += self.pos.z
        return ss

    @property
    def sides(self):
        for v in range(2):
            for d in range(3):
                side = tuple()
                for t in product(range(2), repeat=2):
                    l = list(t)
                    l.insert(d, v)
                    l[0] += self.pos.x
                    l[1] += self.pos.y
                    l[2] += self.pos.z
                    side += (tuple(l),)
                yield side


def read(filename):
    with open(filename, "r") as reader:
        return [Cube(Pos(*map(int, line.strip().split(",")))) for line in reader.readlines()]


if __name__ == "__main__":
    args = sys.argv[1:]
    test = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/18_test.txt")
    else:
        input = read("input/18.txt")

    cubes = input

    sides = [s for c in cubes for s in c.sides]
    n_unique = len(sides) - 2 * (len(sides) - len(set(sides)))
    print(n_unique)
