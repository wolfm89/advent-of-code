#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math


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
    coords = [item for sublist in rocks for item in sublist]
    coords.append(sandhole)
    min_x, max_x = min_max(coords, 0)
    min_y, max_y = min_max(coords, 1)
    print(min_x, max_x, min_y, max_y)
    for y in range(min_y, max_y + 1):
        l = ""
        for x in range(min_x, max_x + 1):
            if (x, y) == sandhole:
                l += "+"
                continue
            if (x, y) in sand:
                l += "o"
                continue
            if (x, y) in coords:
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
        new_rocks.append(new_rock)
    return new_rocks


if __name__ == "__main__":
    sandhole = (500, 0)
    rocks = read("input/14.txt")
    rocks = materialize(rocks)
    sand = []
    draw(rocks, sandhole, sand)
