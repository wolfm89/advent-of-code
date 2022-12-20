#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import copy

DIRS = [(0, 1), (-1, 1), (1, 1)]


def min_max_xy(rocks, sandhole):
    coords = rocks
    coords.append(sandhole)
    min_x, max_x = min_max(coords, 0)
    min_y, max_y = min_max(coords, 1)
    return (min_x, min_y), (max_x, max_y)


def read(filename):
    lines = []
    with open(filename, "r") as reader:
        for line in reader:
            coords = line.strip().split(" -> ")
            coords = [c.split(",") for c in coords]
            coords = [(int(x), int(y)) for x, y in coords]
            lines.append(coords)
    return lines


def min_max(coords, axis):
    min_ = None
    max_ = None
    for coord in coords:
        if min_ is None or coord[axis] < min_:
            min_ = coord[axis]
        if max_ is None or coord[axis] > max_:
            max_ = coord[axis]
    return min_, max_


def draw(rocks, sandhole, sand):
    min_x, max_x = MIN[0], MAX[0]
    min_y, max_y = MIN[1], MAX[1]
    for y in range(min_y, max_y + 1):
        l = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in sand:
                l += "o"
                continue
            if (x, y) == sandhole:
                l += "+"
                continue
            if (x, y) in rocks:
                l += "#"
            else:
                l += "."
        print(l)


def materialize(rocks):
    new_rocks = []
    for rock in rocks:
        new_rock = [rock[0]]
        for p1, p2 in zip(rock, rock[1:]):
            vec = (p2[0] - p1[0], p2[1] - p1[1])
            if vec[0] != 0:
                for x in range(1, abs(vec[0])):
                    new_rock.append((int(p1[0] + math.copysign(x, vec[0])), p1[1]))
            if vec[1] != 0:
                for y in range(1, abs(vec[1])):
                    new_rock.append((p1[0], int(p1[1] + math.copysign(y, vec[1]))))
            new_rock.append(p2)
        new_rocks.extend(new_rock)
    return new_rocks


def move(rocks, sand, s):
    for d in DIRS:
        s_new = (s[0] + d[0], s[1] + d[1])
        if not (s_new in rocks or s_new in sand):
            return s_new
    return s


def simulate_sand(rocks, sand):
    sand_new = copy.deepcopy(sand)
    s_latest = sand_new[-1]
    s_new = move(rocks, sand, s_latest)
    sand_new[-1] = s_new
    return sand_new


if __name__ == "__main__":
    global MIN, MAX
    sandhole = (500, 0)
    rocks = read("input/14.txt")
    rocks = materialize(rocks)
    MIN, MAX = min_max_xy(rocks, sandhole)
    abyss = [(x, MAX[1] + 1) for x in range(MIN[0] - 1, MAX[0] + 2)]
    sand = [sandhole]
    while not any(s in abyss for s in sand):
        sand_new = simulate_sand(rocks, sand)
        if sand_new == sand:
            sand_new.append(sandhole)
        sand = sand_new
        # draw(rocks, sandhole, sand)
        # input("Press key to continue...")
        # print()
    sand = sand[:-1]
    draw(rocks, sandhole, sand)
    print(len(sand))
