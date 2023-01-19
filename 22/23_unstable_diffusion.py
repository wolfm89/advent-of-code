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


N = Vec(x=-1)
S = Vec(x=1)
W = Vec(y=-1)
E = Vec(y=1)
NW = N + W
NE = N + E
SW = S + W
SE = S + E

adjacent_dirs = {
    N: (N, NW, NE),
    S: (S, SW, SE),
    W: (W, NW, SW),
    E: (E, NE, SE),
}

all_adjacent_dirs = (N, S, W, E, NW, NE, SW, SE)


def read(filename: str) -> list[Vec]:
    with open(filename, "r") as reader:
        res = []
        for i, line in enumerate(reader):
            res.extend([Vec(i, j) for j, c in enumerate(line) if c == "#"])
    return res


def propose(elves: list[Vec], directions: list[Vec]) -> tuple[int, list[Vec]]:
    proposals: list[Vec] = []
    i = 0
    for elve in elves:
        done = False
        pos = [elve + d for d in all_adjacent_dirs]
        relevant_elves = [e for e in elves if elve.x - 1 <= e.x <= elve.x + 1 and elve.y - 1 <= e.y <= elve.y + 1]
        if not any(other_elve in pos for other_elve in relevant_elves if other_elve != elve):
            i += 1
            proposals.append(elve)
            continue
        for direction in directions:
            adjacent_pos = [elve + d for d in adjacent_dirs[direction]]
            if not any(other_elve in adjacent_pos for other_elve in relevant_elves if other_elve != elve):
                proposals.append(elve + direction)
                done = True
                break
        if not done:
            proposals.append(elve)
    print(i, "elves haven't moved")
    return i, proposals


def move(elves: list[Vec], proposals: list[Vec]):
    moved_elves: list[Vec] = []
    for i, proposal in enumerate(proposals):
        if proposals.count(proposal) == 1:
            moved_elves.append(proposal)
        else:
            moved_elves.append(elves[i])
    return moved_elves


def plot(elves: list[Vec]) -> None:
    x_max, y_max, x_min, y_min = min_max_pos(elves)

    for i in range(x_min, x_max + 1):
        line = "".join(["#" if Vec(i, j) in elves else "." for j in range(y_min, y_max + 1)])
        print(line)
    print()


def min_max_pos(positions: list[Vec]) -> tuple[int, int, int, int]:
    x_max = max(positions, key=lambda p: p.x).x
    y_max = max(positions, key=lambda p: p.y).y
    x_min = min(positions, key=lambda p: p.x).x
    y_min = min(positions, key=lambda p: p.y).y
    return x_max, y_max, x_min, y_min


def result(elves: list[Vec]) -> int:
    x_max, y_max, x_min, y_min = min_max_pos(elves)
    return (x_max - x_min + 1) * (y_max - y_min + 1) - len(elves)


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
    n_elves = len(elves)
    print(n_elves, "elves")

    directions = [N, S, W, E]

    if test:
        plot(elves)
    i = 0
    while True:
        print("Round", i + 1)
        elves.sort(key=lambda e: (e.x, e.y))
        havent_moved, proposals = propose(elves, directions)
        if havent_moved == n_elves:
            break
        elves = move(elves, proposals)
        if test:
            plot(elves)
        if i == 9:
            print(result(elves))
        directions = directions[1:] + directions[:1]
        i += 1
    print(i + 1)
