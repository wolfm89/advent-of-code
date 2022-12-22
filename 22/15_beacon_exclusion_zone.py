#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import math


def read(filename):
    sensors, beacons = [], []
    with open(filename, "r") as reader:
        for line in reader:
            numbers = [int(s) for s in re.findall(r"-?\d+", line.strip())]
            sensors.append((numbers[0], numbers[1]))
            beacons.append((numbers[2], numbers[3]))
    return sensors, beacons


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def min_max(axis, sensors, distances):
    min_, max_ = math.inf, -math.inf
    for s, d in zip(sensors, distances):
        lower = s[axis] - d
        if lower < min_:
            min_ = lower
        upper = s[axis] + d
        if upper > max_:
            max_ = upper
    return min_, max_


def draw(X, Y, sensors, distances):
    N = 2
    max_digits_x = max(n_digits(X[0]), n_digits(X[1]))
    max_digits_y = max(n_digits(Y[0]), n_digits(Y[1]))
    for i in reversed(range(1, max_digits_x + 1)):
        l = " " * max_digits_y
        for x in range(X[0], X[1] + 1):
            if x % N == 0:
                nd = n_digits(x)
                if nd < i:
                    l += " "
                else:
                    if nd == i and x < 0:
                        l += "-"
                    else:
                        l += str(digit(abs(x), i))
            else:
                l += " "
        print(l)

    for y in range(Y[0], Y[1] + 1):
        if y % N == 0:
            l = str(y).rjust(max_digits_y)
        else:
            l = " " * max_digits_y
        for x in range(X[0], X[1] + 1):
            if (x, y) in sensors:
                l += "S"
            elif (x, y) in beacons:
                l += "B"
            elif any(dist(s, (x, y)) <= d for s, d in zip(sensors, distances)):
                l += "#"
            else:
                l += "."
        print(l)


def n_digits(i):
    return 1 if i == 0 else (int(math.log(abs(i), 10)) + 1 + (1 if i < 0 else 0))


def digit(number, n):
    return number // 10 ** (n - 1) % 10


def no_beacons_at(sensors, distances, y):
    ranges = []
    for s, d in zip(sensors, distances):
        x_diff = d - abs(s[1] - y)
        if x_diff >= 0:
            ranges.append((s[0] - x_diff, s[0] + x_diff))

    union_ranges = []
    for begin, end in sorted(ranges):
        if union_ranges and union_ranges[-1][1] >= begin - 1:
            union_ranges[-1][1] = max(union_ranges[-1][1], end)
        else:
            union_ranges.append([begin, end])

    return union_ranges


if __name__ == "__main__":
    args = sys.argv[1:]
    test = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        sensors, beacons = read("input/15_test.txt")
        y = 10
    else:
        sensors, beacons = read("input/15.txt")
        y = 2_000_000

    distances = [dist(s, b) for s, b in zip(sensors, beacons)]
    min_x, max_x = min_max(0, sensors, distances)
    min_y, max_y = min_max(1, sensors, distances)

    if test:
        draw((min_x, max_x), (min_y, max_y), sensors, distances)

    n_no_beacons_pos = 0
    impossible_beacon_ranges = no_beacons_at(sensors, distances, y=y)
    for r in impossible_beacon_ranges:
        n_no_beacons_pos += r[1] - r[0] + 1
    n_no_beacons_pos -= sum(1 for b in set(beacons) if b[1] == y)
    print(n_no_beacons_pos)
