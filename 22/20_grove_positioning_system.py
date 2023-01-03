#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from copy import copy


def read(filename: str) -> list[int]:
    with open(filename, "r") as reader:
        for line in reader:
            yield int(line.strip())


def solve(data, test):
    L = len(data)
    moved: list[bool] = [False] * L
    while not all(moved):
        if test:
            print(data)
        idx = moved.index(False)
        d = data[idx] % (L - 1)
        new_idx = idx + d + 1
        if new_idx > L:
            new_idx -= L
        data.insert(new_idx, data[idx])
        moved.insert(new_idx, True)
        if new_idx <= idx:
            del data[idx + 1]
            del moved[idx + 1]
        else:
            del data[idx]
            del moved[idx]
    if test:
        print(data)


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    test: bool = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/20_test.txt")
    else:
        input = read("input/20.txt")

    data: list[int] = list(input)
    data2: list[int] = copy(data)
    L = len(data)

    # data = [3, 1, 0]
    # data = [0, -1, -1, 1]
    # L = len(data)
    # moved: list[bool] = [False] * L

    # Part 1
    solve(data, test)
    idx_zero = data.index(0)
    idx_coords = [1000, 2000, 3000]
    coords = []
    for idx_coord in idx_coords:
        idx_dist = idx_coord % L
        idx = idx_zero + idx_dist
        if idx > L - 1:
            idx -= L
        coords.append(data[idx])
    print(coords)
    print(sum(coords))

    # Part 2
    # data2 = [n * 811589153 for n in data2]
    # L = len(data2)
    # for i in range(10):
