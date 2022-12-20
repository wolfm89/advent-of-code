#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

DIRS = [(0, 1), (-1, 1), (1, 1)]


def min_max_xy(rocks, sandhole, floor=None):
    coords = rocks
    coords.append(sandhole)
    min_x, max_x = min_max(coords, 0)
    min_y, max_y = min_max(coords, 1)
    if floor is not None:
        max_y = floor
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


def draw(rocks, sandhole, sand, floor=None):
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
            if (x, y) in rocks or y == floor:
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


def simulate(rocks, sandhole, condition, sand, floor=None):
    i = 1
    while True:
        s = sand[-1]
        if s[1] == MAX[1]:
            s_new = s
        else:
            for d in DIRS:
                s_new = (s[0] + d[0], s[1] + d[1])
                if (floor is None or not s_new[1] == floor) and not (s_new in sand) and not (s_new in rocks):
                    break
                else:
                    s_new = s
        if condition(s_new, sandhole):
            break
        if s_new == sand[-1]:
            sand.append(sandhole)
        else:
            sand[-1] = s_new
        # draw(rocks, sandhole, sand)
        # input("Press key to continue...")
        # print()
        if i % 10000 == 0:
            print(i, len(sand))
        i += 1
    return sand[:-1]


def condition1(s, _):
    return s[1] == MAX[1] or s[0] == MIN[0] or s[0] == MAX[0]


def condition2(s, sandhole):
    return s == sandhole


if __name__ == "__main__":
    global MIN, MAX
    sandhole = (500, 0)

    rocks = read("input/14.txt")
    rocks = materialize(rocks)
    MIN, MAX = min_max_xy(rocks, sandhole)

    sand = [sandhole]
    draw(rocks, sandhole, [])
    print()
    sand = simulate(rocks, sandhole, condition1, sand)
    draw(rocks, sandhole, sand)
    print(len(sand))
    print()

    floor = MAX[1] + 2
    MIN, MAX = min_max_xy(rocks, sandhole, floor=floor)
    sand = [sandhole]
    draw(rocks, sandhole, [])
    print()
    sand = simulate(rocks, sandhole, condition2, sand, floor=floor)
    draw(rocks, sandhole, sand, floor=floor)
    print(len(sand))
