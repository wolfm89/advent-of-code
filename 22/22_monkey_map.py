#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import operator
import re
import sys
from dataclasses import dataclass, field
from itertools import cycle, product
from typing import Any, Iterator, Optional, Union

Map = list[str]
Cmd = Union[int, str]


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

    def __mul__(self, other: Union[Union[float, int], Vec]) -> Vec:
        if isinstance(other, (float, int)):
            return Vec(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vec):
            return Vec(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
            )
        else:
            raise ValueError()

    def __truediv__(self, f: float) -> Vec:
        return Vec(self.x / f, self.y / f, self.z / f)

    def __matmul__(self, other: Vec) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def index(self, val: Any, op=operator.eq) -> int:
        return next(j for j, v in enumerate(self) if op(v, val))

    def rot(self, ax: Vec, shift: Vec = None, n: int = 1) -> Vec:
        if shift is None:
            shift = Vec()
        i_not_0 = ax.index(0.0, operator.ne)
        diff = NO[i_not_0] @ shift
        p = self
        for _ in range(n):
            p = ROT[ax] @ (p - diff) + diff
        return p


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


@dataclass
class Area:
    pos_lu_orig: Vec
    pos_lu: Vec
    map: Map
    pos_rd: Vec = field(init=False)
    facing: Vec = Z
    neighbors: list[Area] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)

    def __post_init__(self):
        self.pos_rd = self.pos_lu + X + Y

    @property
    def center(self) -> Vec:
        return (self.pos_lu + self.pos_rd) / 2

    @property
    def pos_ru(self) -> Vec:
        return self.__rot_lu(3)

    @property
    def pos_ld(self) -> Vec:
        return self.__rot_lu()

    def __rot_lu(self, n: int = 1) -> Vec:
        return self.pos_lu.rot(self.facing, self.center, n)

    @property
    def corners(self) -> tuple[Vec, Vec, Vec, Vec]:
        return (self.pos_lu, self.pos_ld, self.pos_rd, self.pos_ru)


@dataclass
class Edge:
    pos: Vec
    facing: Vec
    neighbors: list[Area] = field(default_factory=list)


def read(filename: str) -> tuple[Map, list[Cmd]]:
    with open(filename, "r") as reader:
        map: Map = []
        for line in reader:
            if not line.strip():
                break
            map.append(line.rstrip())
        len_max = max(len(l) for l in map)
        map = [l.ljust(len_max) for l in map]
        cmds = reader.readline().strip()
        last_no = re.search(r"\d+$", cmds)
        res = re.findall(r"(\d+)(R|L)", cmds) + ([(last_no.group(),)] if last_no is not None else [])
        return map, [int(c) if c.isnumeric() else c for cmds in res for c in cmds]


def in_bounds(pos: Vec, max0: int, max1: int) -> bool:
    return 0 <= pos.x <= max0 and 0 <= pos.y <= max1


def plot(map: Map, pos: Optional[Vec] = None) -> None:
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
        if abs(area.pos_lu.y - a.pos_lu.y) == 1:
            y = area.pos_lu.y if area.pos_lu.y - a.pos_lu.y == 1 else a.pos_lu.y
            facing = X if y < initial_pos.y else -X
            edge = Edge(Vec(area.pos_lu.x + 0.5, y, 0), facing, [area, a])
        area.edges.append(edge)
        a.edges.append(edge)


def read_areas(l: int, map: Map) -> Iterator[Area]:
    for i, j in product(range(0, len(map), l), range(0, len(map[0]), l)):
        if map[i][j] != " ":
            yield Area(Vec(i, j), Vec(float(i // l), float(j // l), 0), [line[j : j + l] for line in map[i : i + l]])


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


def solve1(test: bool, map: Map, cmds: list[Cmd], pos: Vec, dir: Vec) -> tuple[Vec, Vec]:
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
        for area, _ in trace_neighbors(edge.neighbors[1], edge.neighbors[0]):
            area.facing = area.facing.rot(edge.facing)
            area.pos_lu = area.pos_lu.rot(edge.facing, edge.pos)
            area.pos_rd = area.pos_rd.rot(edge.facing, edge.pos)
        for e in trace_edges(edge.neighbors[1], edge.neighbors[0]):
            e.facing = e.facing.rot(edge.facing)
            e.pos = e.pos.rot(edge.facing, edge.pos)


def complete_edges_and_areas(areas: list[Area]):
    for area in areas:
        complete_edges(area)
    complete_areas(areas)


def complete_areas(areas: list[Area]):
    for area in areas:
        area.neighbors = []
        for edge in area.edges:
            neighbor = next(a for a in areas if edge.pos in (e.pos for e in a.edges) and a != area)
            area.neighbors.append(neighbor)
            if area not in edge.neighbors:
                edge.neighbors.append(area)
            if neighbor not in edge.neighbors:
                edge.neighbors.append(neighbor)


def complete_edges(area: Area):
    corners = area.corners
    corners1 = cycle(corners)
    next(corners1)
    edges = []
    for ends in zip(corners, corners1):
        c1, c2 = ends
        edge = Edge((c1 + c2) / 2, c2 - c1, [area])
        edges.append(edge)
    area.edges = edges


def solve2(test: bool, map: Map, cmds: list[Cmd], pos: Vec, area: Area, dir: Vec) -> tuple[Vec, Vec]:
    p_max = len(area.map) - 1

    dir_neigh_map = dict((d, i) for i, d in enumerate([-Y, X, Y, -X]))

    for cmd in cmds:
        if isinstance(cmd, int):
            while cmd:  # cmd is number of steps and will count down to 0
                new_pos = pos + dir
                new_area = area
                new_dir = dir
                if not in_bounds(new_pos, p_max, p_max):
                    i = dir_neigh_map[dir]
                    edge = area.edges[i]
                    new_area = next(n for n in edge.neighbors if n != area)
                    new_i = next(i for i, e in enumerate(new_area.edges) if e.pos == edge.pos)
                    n_rot = (new_i + 2 - i) % 4
                    new_pos = new_pos - dir * (p_max + 1)
                    new_pos = new_pos.rot(Z, Vec(p_max / 2, p_max / 2), n_rot)
                    new_dir = new_dir.rot(Z, n=n_rot)
                if new_area.map[int(new_pos.x)][int(new_pos.y)] == "#":
                    break
                else:
                    cmd -= 1
                area = new_area
                pos = new_pos
                dir = new_dir
            if test:
                plot(map, area.pos_lu_orig + pos)
        else:
            if cmd == "R":
                dir = ROT[-Z] @ dir
            else:
                dir = ROT[Z] @ dir
    return area.pos_lu_orig + pos, dir


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

    d = {Y: 0, X: 1, -Y: 2, -X: 3}
    password = lambda pos, dir: 1000 * (pos.x + 1) + 4 * (pos.y + 1) + d[dir]

    ### Part 1

    pos = Vec(0, map[0].index("."))
    dir = Y

    pos, dir = solve1(test, map, cmds, pos, dir)
    print(password(pos, dir))

    ### Part 2

    # Create cube faces and edges
    areas: list[Area] = list(read_areas(L, map))
    set_neighbors(areas)
    set_edges(areas)
    edges: list[Edge] = list(trace_edges(areas[0], None))

    fold_cube(edges)

    complete_edges_and_areas(areas)

    pos = Vec(0, 0)  # starting position
    a = areas[0]
    dir = Y

    pos, dir = solve2(test, map, cmds, pos, a, dir)
    print(int(password(pos, dir)))
