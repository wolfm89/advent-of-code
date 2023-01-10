#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import sys
import operator
from typing import Union, Optional, Iterator, Any
import re
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Vec:
    x: float = 0
    y: float = 0
    z: float = 0

    @property
    def len(self):
        return 3

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other: Vec) -> Vec:
        return Vec(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec) -> Vec:
        return Vec(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> Vec:
        return Vec(-self.x, -self.y, -self.z)

    def __mul__(self, other: Vec) -> Vec:
        return Vec(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def __truediv__(self, f: float) -> Vec:
        return Vec(self.x / f, self.y / f, self.z / f)

    def __matmul__(self, other: Vec) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def index(self, val: Any, op=operator.eq) -> int:
        return next(j for j, v in enumerate(self) if op(v, val))


@dataclass(frozen=True)
class Matrix:
    rows: list[Vec]

    def __matmul__(self, other: Vec) -> Vec:
        if self.rows[0].len != other.len:
            raise ValueError()
        return Vec(*[vec @ other for vec in self.rows])


X = Vec(x=1)
Y = Vec(y=1)
Z = Vec(z=1)
ZERO = Vec()
ONE = X + Y + Z

NO_X = Matrix([ZERO, Y, Z])
NO_Y = Matrix([X, ZERO, Z])
NO_Z = Matrix([X, Y, ZERO])

NO = (NO_X, NO_Y, NO_Z)

ROT_X_CCW = Matrix([X, -Z, Y])
ROT_X_CW = Matrix([X, Z, -Y])
ROT_Y_CCW = Matrix([Z, Y, -X])
ROT_Y_CW = Matrix([-Z, Y, X])
ROT_Z_CCW = Matrix([-Y, X, Z])
ROT_Z_CW = Matrix([Y, -X, Z])

ROT = {
    X: ROT_X_CCW,
    -X: ROT_X_CW,
    Y: ROT_Y_CCW,
    -Y: ROT_Y_CW,
    Z: ROT_Z_CCW,
    -Z: ROT_Z_CW,
}


class Area:
    def __init__(
        self,
        pos_lu: Vec,
        map: list[str],
        facing: Vec = Z,
        neighbors: list[Area] = None,
        edges: list[Area] = None,
    ) -> None:
        self.pos_lu = pos_lu
        self.pos_rd = pos_lu + X + Y
        self.map = map
        self.facing = facing
        self.neighbors = neighbors if neighbors is not None else list()
        self.edges = edges if edges is not None else list()


class Edge:
    def __init__(self, pos: Vec, facing: Vec, neighbors: list[Area] = None) -> None:
        self.pos = pos
        self.facing = facing
        self.neighbors = neighbors if neighbors is not None else list()


def read(filename: str) -> tuple[list[str], list[Union[int, str]]]:
    with open(filename, "r") as reader:
        map: list[str] = []
        for line in reader:
            if not line.strip():
                break
            map.append(line.rstrip())
        len_max = max(len(l) for l in map)
        map = [l.ljust(len_max) for l in map]
        cmds = reader.readline().strip()
        res = re.findall(r"(\d+)(R|L)", cmds) + [(re.search(r"\d+$", cmds).group(),)]
        return map, [int(c) if c.isnumeric() else c for cmds in res for c in cmds]


def in_bounds(pos: Vec, max0: int, max1: int) -> bool:
    return 0 <= pos.x <= max0 and 0 <= pos.y <= max1


def plot(map: tuple[list[str]], pos: Optional[Vec] = None) -> None:
    for i, l in enumerate(map):
        if pos is not None and pos.x == i:
            l = "".join([c if i != pos.y else "*" for i, c in enumerate(l)])
        print(l)
    print()


def set_neighbors(areas: list[Area]) -> None:
    for area in areas:
        n = next((a for a in areas if Vec(area.pos_lu.x + 1, area.pos_lu.y, 0) == a.pos_lu), None)
        if n is not None:
            area.neighbors.append(n)
            n.neighbors.append(area)
        n = next((a for a in areas if Vec(area.pos_lu.x, area.pos_lu.y + 1, 0) == a.pos_lu), None)
        if n is not None:
            area.neighbors.append(n)
            n.neighbors.append(area)


def set_edges(areas: list[Area]) -> None:
    initial_pos = (areas[0].pos_lu + areas[0].pos_rd) / 2.0
    skip_first = True
    for a, area in trace_neighbors(areas[0], None):
        a: Area
        area: Area
        if skip_first:
            skip_first = False
            continue
        if abs(area.pos_lu.x - a.pos_lu.x) == 1:
            x = area.pos_lu.x if area.pos_lu.x - a.pos_lu.x == 1 else a.pos_lu.x
            facing = Y if x > initial_pos.x else -Y
            edge = Edge(Vec(x, area.pos_lu.y + 0.5, 0), facing, [area, a])
            area.edges.append(edge)
            a.edges.append(edge)
        if abs(area.pos_lu.y - a.pos_lu.y) == 1:
            y = area.pos_lu.y if area.pos_lu.y - a.pos_lu.y == 1 else a.pos_lu.y
            facing = X if y < initial_pos.y else -X
            edge = Edge(Vec(area.pos_lu.x + 0.5, y, 0), facing, [area, a])
            area.edges.append(edge)
            a.edges.append(edge)


def read_areas(l: int, map: list[str]) -> Iterator[Area]:
    for i, j in product(range(0, len(map), l), range(0, len(map[0]), l)):
        if map[i][j] != " ":
            yield Area(Vec(float(i // l), float(j // l), 0), [line[j : j + l] for line in map[i : i + l]])


def trace_neighbors(start: Area, from_area: Area) -> Iterator[tuple[Area, Area]]:
    yield start, from_area
    for n in start.neighbors:
        if n != from_area:
            yield from trace_neighbors(n, start)


def trace_edges(start: Area, from_area: Area) -> Iterator[Edge]:
    for e in start.edges:
        if from_area is None or e not in from_area.edges:
            yield e
    for n in start.neighbors:
        if n != from_area:
            yield from trace_edges(n, start)


def solve1(test: bool, map: list[str], cmds: list[Union[int, str]], pos: Vec, dir: Vec) -> tuple[Vec, Vec]:
    max0 = len(map) - 1
    max1 = len(map[0]) - 1

    for cmd in cmds:
        if isinstance(cmd, int):
            last_valid_pos: Optional[Vec] = None
            while cmd:
                new_pos = pos + dir
                if not in_bounds(new_pos, max0, max1):
                    if dir in (X, Y):
                        new_pos = Vec(0, new_pos.y) if dir.index(0) == 1 else Vec(new_pos.x, 0)
                    else:
                        new_pos = Vec(max0, new_pos.y) if dir.index(0) == 1 else Vec(new_pos.x, max1)
                if map[new_pos.x][new_pos.y] == "#":
                    if last_valid_pos is not None:
                        pos = last_valid_pos
                    break
                if map[new_pos.x][new_pos.y] == " ":
                    last_valid_pos = pos if last_valid_pos is None else last_valid_pos
                else:
                    last_valid_pos = None
                    cmd -= 1
                pos = new_pos
            if test:
                plot(map, pos)
        else:
            if cmd == "R":
                dir = ROT[-Z] @ dir
            else:
                dir = ROT[Z] @ dir
    return pos, dir


def fold_cube(edges: list[Edge]):
    for edge in edges:
        i_not_0 = edge.facing.index(0.0, operator.ne)
        diff = NO[i_not_0] @ edge.pos
        for area, _ in trace_neighbors(edge.neighbors[1], edge.neighbors[0]):
            area.facing = ROT[edge.facing] @ area.facing
            area.pos_lu = ROT[edge.facing] @ (area.pos_lu - diff) + diff
            area.pos_rd = ROT[edge.facing] @ (area.pos_rd - diff) + diff
        for e in trace_edges(edge.neighbors[1], edge.neighbors[0]):
            e.facing = ROT[edge.facing] @ e.facing
            e.pos = ROT[edge.facing] @ (e.pos - diff) + diff


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    test: bool = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/22_test.txt")
        L = 4
    else:
        input = read("input/22.txt")
        L = 50

    map, cmds = input

    ### Part 1

    pos = Vec(0, map[0].index("."))
    dir = Y
    pos, dir = solve1(test, map, cmds, pos, dir)

    d = {Y: 0, X: 1, -Y: 2, -X: 3}
    password = 1000 * (pos.x + 1) + 4 * (pos.y + 1) + d[dir]
    print(password)

    ### Part 2

    # Create cube faces and edges
    areas: list[Area] = list(read_areas(L, map))
    set_neighbors(areas)
    set_edges(areas)
    edges: list[Edge] = list(trace_edges(areas[0], None))

    # Fold cube
    fold_cube(edges)

    for area in areas:
        print(f"{area.pos_lu}, {area.pos_rd}: {area.facing}")
