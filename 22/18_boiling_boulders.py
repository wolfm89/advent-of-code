#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import NamedTuple
from itertools import product
from collections import deque


class Pos(NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0

    @classmethod
    def from_iterable(cls, t):
        return cls(t[0], t[1], t[2])

    def t(self):
        return self.x, self.y, self.z

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y, self.z - other.z)


class Cube(NamedTuple):
    pos: Pos

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

    @property
    def neighbours(self):
        for i in range(3):
            l = [0, 0]
            l.insert(i, 1)
            yield Cube(self.pos + Pos.from_iterable(l))
            yield Cube(self.pos - Pos.from_iterable(l))

    def inside(self, start, end):
        return start.x <= self.pos.x <= end.x and start.y <= self.pos.y <= end.y and start.z <= self.pos.z <= end.z


def read(filename):
    with open(filename, "r") as reader:
        return [Cube(Pos(*map(int, line.strip().split(",")))) for line in reader.readlines()]


def bfs(cubes, start, end):
    queue = deque([start])
    visited = [start]

    while queue:
        cube = queue.popleft()
        for c in cube.neighbours:
            if not c in visited and c.inside(start.pos, end.pos) and c not in cubes:
                visited.append(c)
                queue.append(c)
    return visited


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

    min_x = min(c.pos.x for c in cubes)
    max_x = max(c.pos.x for c in cubes)
    min_y = min(c.pos.y for c in cubes)
    max_y = max(c.pos.y for c in cubes)
    min_z = min(c.pos.z for c in cubes)
    max_z = max(c.pos.z for c in cubes)
    min_ = Pos(min_x, min_y, min_z) - Pos(1, 1, 1)
    max_ = Pos(max_x, max_y, max_z) + Pos(1, 1, 1)

    outside_cubes = bfs(cubes, Cube(min_), Cube(max_))
    sides = [s for c in outside_cubes for s in c.sides]
    n_unique = len(sides) - 2 * (len(sides) - len(set(sides)))
    space = max_ - min_ + Pos(1, 1, 1)
    space_boundary_area = 2 * space.x * space.y + 2 * space.x * space.z + 2 * space.y * space.z
    print(n_unique - space_boundary_area)
