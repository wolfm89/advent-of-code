#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import product


def read(filename):
    lines = []
    with open(filename, "r") as reader:
        for line in reader:
            lines.append(line.strip())
    return lines


def check_visible(grid, position):
    return all(h < grid[position[0]][position[1]] for h in grid[position[0]][: position[1]])


def viewing_distance(grid, position):
    try:
        return [h < grid[position[0]][position[1]] for h in reversed(grid[position[0]][: position[1]])].index(False) + 1
    except ValueError:
        return position[1]


if __name__ == "__main__":
    grid = read("input/8.txt")
    grid_f = [l[::-1] for l in grid]
    grid_t = list(map(list, zip(*grid)))  # transpose
    grid_f_t = [l[::-1] for l in grid_t]

    n_visible = sum(
        check_visible(grid, (i, j))
        or check_visible(grid_t, (j, i))
        or check_visible(grid_f, (i, len(grid_t) - j - 1))
        or check_visible(grid_f_t, (j, len(grid) - i - 1))
        for i, j in product(range(len(grid)), range(len(grid_t)))
    )
    print(n_visible)

    max_scenic_score = max(
        viewing_distance(grid, (i, j))
        * viewing_distance(grid_t, (j, i))
        * viewing_distance(grid_f, (i, len(grid_t) - j - 1))
        * viewing_distance(grid_f_t, (j, len(grid) - i - 1))
        for i, j in product(range(len(grid)), range(len(grid_t)))
    )
    print(max_scenic_score)
