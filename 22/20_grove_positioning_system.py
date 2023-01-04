#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from copy import copy


def read(filename: str) -> list[int]:
    with open(filename, "r") as reader:
        for line in reader:
            yield int(line.strip())


def solve(L: int, data: list[int], order: list[int], test: bool) -> None:
    for i in range(L):
        if test:
            print(data)
        idx = order.index(i)
        d = data[idx] % (L - 1)
        new_idx = idx + d + 1
        if new_idx > L:
            new_idx -= L
        data.insert(new_idx, data[idx])
        order.insert(new_idx, i)
        if new_idx <= idx:
            del data[idx + 1]
            del order[idx + 1]
        else:
            del data[idx]
            del order[idx]
    if test:
        print(data)


def get_coords(L: int, data: list[int], idx_coords: list[int]) -> list[int]:
    idx_zero = data.index(0)
    for idx_coord in idx_coords:
        idx_dist = idx_coord % L
        idx = idx_zero + idx_dist
        if idx > L - 1:
            idx -= L
        yield data[idx]


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
    idx_coords = [1000, 2000, 3000]

    # Part 1
    order: list[int] = list(range(L))
    solve(L, data, order, test)
    coords = list(get_coords(L, data, idx_coords))
    print(coords)
    print(sum(coords))

    # Part 2
    data2 = [n * 811589153 for n in data2]
    order: list[int] = list(range(L))
    for i in range(10):
        solve(L, data2, order, test)
    coords = list(get_coords(L, data2, idx_coords))
    print(coords)
    print(sum(coords))
