#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import Union, Optional
import re


def read(filename: str) -> tuple[list[str], list[Union[int, str]]]:
    with open(filename, "r") as reader:
        map = []
        for line in reader:
            if not line.strip():
                break
            map.append(line.rstrip())
        len_max = max(len(l) for l in map)
        map = [l.ljust(len_max) for l in map]
        cmds = reader.readline().strip()
        res = re.findall(r"(\d+)(R|L)", cmds) + [(re.search(r"\d+$", cmds).group(),)]
        return map, [int(c) if c.isnumeric() else c for cmds in res for c in cmds]


def mv(pos: tuple[int, int], dir: tuple[int, int]) -> tuple[int, int]:
    return (pos[0] + dir[0], pos[1] + dir[1])


def in_bounds(pos: tuple[int, int], max0: int, max1: int) -> bool:
    return 0 <= pos[0] <= max0 and 0 <= pos[1] <= max1


def plot(map: tuple[list[str]], pos: Optional[tuple[int, int]] = None) -> None:
    for i, l in enumerate(map):
        if pos is not None and pos[0] == i:
            l = "".join([c if i != pos[1] else "*" for i, c in enumerate(l)])
        print(l)
    print()


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    test: bool = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/22_test.txt")
    else:
        input = read("input/22.txt")

    map, cmds = input

    pos = (0, map[0].index("."))
    dir = (0, 1)

    max0 = len(map) - 1
    max1 = len(map[0]) - 1

    for cmd in cmds:
        if isinstance(cmd, int):
            last_valid_pos: Optional[tuple[int, int]] = None
            while cmd:
                new_pos = mv(pos, dir)
                if not in_bounds(new_pos, max0, max1):
                    if dir in ((1, 0), (0, 1)):
                        new_pos = (0, new_pos[1]) if dir.index(0) == 1 else (new_pos[0], 0)
                    else:
                        new_pos = (max0, new_pos[1]) if dir.index(0) == 1 else (new_pos[0], max1)
                if map[new_pos[0]][new_pos[1]] == "#":
                    if last_valid_pos is not None:
                        pos = last_valid_pos
                    break
                if map[new_pos[0]][new_pos[1]] == " ":
                    last_valid_pos = pos if last_valid_pos is None else last_valid_pos
                else:
                    last_valid_pos = None
                    cmd -= 1
                pos = new_pos
            if test:
                plot(map, pos)
        else:
            if cmd == "R":
                dir = (dir[1], -dir[0])
            else:
                dir = (-dir[1], dir[0])

    d = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}
    password = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + d[dir]
    print(password)
