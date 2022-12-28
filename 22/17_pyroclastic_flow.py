#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
from enum import Enum
from itertools import cycle


class Dir(Enum):
    R = (1, 0)
    L = (-1, 0)
    U = (0, 1)
    D = (0, -1)

    @classmethod
    def from_char(cls, c):
        return cls.L if c == "<" else cls.R if c == ">" else None


class Shape(Enum):
    HBAR = {((0, 0), (3, 0))}
    PLUS = {((0, 1), (2, 1)), ((1, 0), (1, 2))}
    REVL = {((0, 0), (2, 0)), ((2, 0), (2, 2))}
    VBAR = {((0, 0), (0, 3))}
    SQUR = {((0, 0), (1, 0)), ((0, 1), (1, 1))}

    def __init__(self, dim):
        self.dim = dim
        self.max_x = max(p[0] for l in self.dim for p in l)
        self.max_y = max(p[1] for l in self.dim for p in l)


class Rock:
    X_MIN = 0
    X_MAX = 6

    def __init__(self, shape, pos):
        self.shape = shape
        self.pos = pos

    def move(self, dir, rocks):
        new_x = self.pos[0] + dir.value[0]
        new_y = self.pos[1] + dir.value[1]
        if new_y < 0 or new_x < 0 or new_x + self.shape.max_x > self.X_MAX or self.intersects(new_x, new_y, rocks):
            return False
        else:
            self.pos = (new_x, new_y)
            return True

    def intersects(self, x, y, rocks):
        for rock in rocks:
            for line1 in rock.shape.value:
                line1A = (rock.pos[0] + line1[0][0], rock.pos[1] + line1[0][1])
                line1B = (rock.pos[0] + line1[1][0], rock.pos[1] + line1[1][1])
                for line2 in self.shape.value:
                    line2A = (x + line2[0][0], y + line2[0][1])
                    line2B = (x + line2[1][0], y + line2[1][1])
                    if Rock.lines_intersect(line1A, line1B, line2A, line2B):
                        return True
        return False

    @staticmethod
    def on_segment(p, q, r):
        if (
            (q[0] <= max(p[0], r[0]))
            and (q[0] >= min(p[0], r[0]))
            and (q[1] <= max(p[1], r[1]))
            and (q[1] >= min(p[1], r[1]))
        ):
            return True
        return False

    @staticmethod
    def orientation(p, q, r):
        # to find the orientation of an ordered triplet (p,q,r)
        # function returns the following values:
        # 0 : Collinear points
        # 1 : Clockwise points
        # 2 : Counterclockwise

        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
        # for details of below formula.

        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
        if val > 0:

            # Clockwise orientation
            return 1
        elif val < 0:

            # Counterclockwise orientation
            return 2
        else:

            # Collinear orientation
            return 0

    # The main function that returns true if
    # the line segment 'p1q1' and 'p2q2' intersect.
    @staticmethod
    def lines_intersect(p1, q1, p2, q2):

        # Find the 4 orientations required for
        # the general and special cases
        o1 = Rock.orientation(p1, q1, p2)
        o2 = Rock.orientation(p1, q1, q2)
        o3 = Rock.orientation(p2, q2, p1)
        o4 = Rock.orientation(p2, q2, q1)

        # General case
        if (o1 != o2) and (o3 != o4):
            return True

        # Special Cases

        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if (o1 == 0) and Rock.on_segment(p1, p2, q1):
            return True

        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if (o2 == 0) and Rock.on_segment(p1, q2, q1):
            return True

        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if (o3 == 0) and Rock.on_segment(p2, p1, q2):
            return True

        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if (o4 == 0) and Rock.on_segment(p2, q1, q2):
            return True

        # If none of the cases
        return False

    @property
    def max_y(self):
        return self.pos[1] + self.shape.max_y

    def __str__(self):
        return f"{str(self.shape)}, {str(self.pos)}"


def read(filename):
    with open(filename, "r") as reader:
        return [Dir.from_char(c) for c in reader.readline().strip()]


if __name__ == "__main__":
    args = sys.argv[1:]
    test = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/17_test.txt")
    else:
        input = read("input/17.txt")

    jet_directions = input

    MAX_N_ROCKS = 2022
    X_L_START = 2
    Y_GAP_START = 4

    directions = cycle(jet_directions)
    rocks = []
    for shape in cycle(Shape):
        rock = Rock(shape, (X_L_START, max([rock.max_y for rock in rocks], default=-1) + Y_GAP_START))
        while True:
            dir = next(directions)
            rock.move(dir, rocks)
            if not rock.move(Dir.D, rocks):
                break
        rocks.append(rock)
        n = len(rocks)
        if n % math.ceil(MAX_N_ROCKS / 100) == 0:
            print(f"{round(n / MAX_N_ROCKS * 100)}%", end="\r", flush=True)
        if n == MAX_N_ROCKS:
            break

    print()
    print(max([rock.max_y for rock in rocks]) + 1)
