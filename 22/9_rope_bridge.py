#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class Dir(Enum):
    U = (0, 1)
    D = (0, -1)
    L = (-1, 0)
    R = (1, 0)


def read(filename):
    movements = []
    with open(filename, "r") as reader:
        for line in reader:
            dir, steps = line.strip().split(" ")
            movements.append((Dir[dir], int(steps)))
    return movements


def m(pos, dir, n=1):
    return (pos[0] + dir.value[0] * n, pos[1] + dir.value[1] * n)


def touches(p1, p2):
    return (
        p2 == p1
        or p2 == m(m(p1, Dir.U), Dir.L)
        or p2 == m(p1, Dir.U)
        or p2 == m(m(p1, Dir.U), Dir.R)
        or p2 == m(p1, Dir.L)
        or p2 == m(p1, Dir.R)
        or p2 == m(m(p1, Dir.D), Dir.L)
        or p2 == m(p1, Dir.D)
        or p2 == m(m(p1, Dir.D), Dir.R)
    )


def move(pos_h, pos_t, dir):
    pos_h_new = m(pos_h, dir)
    if touches(pos_h_new, pos_t):
        return pos_h_new, pos_t
    if pos_h[0] == pos_t[0] or pos_h[1] == pos_t[1]:  # H and T on same row or column
        pos_t_new = m(pos_t, dir)
    else:
        pos_t_new = m(pos_t, dir)
        if dir == Dir.U or dir == Dir.D:
            pos_t_new = m(pos_t_new, Dir.L if pos_h_new[0] < pos_t_new[0] else Dir.R)
        else:
            pos_t_new = m(pos_t_new, Dir.U if pos_h_new[1] > pos_t_new[1] else Dir.D)
    return pos_h_new, pos_t_new


def pretty_print(tail_visited):
    max_x = max(tail_visited, key=lambda p: p[0])[0]
    min_x = min(tail_visited, key=lambda p: p[0])[0]
    max_y = max(tail_visited, key=lambda p: p[1])[1]
    min_y = min(tail_visited, key=lambda p: p[1])[1]
    for j in range(max_y, min_y - 1, -1):
        l = ""
        for i in range(min_x, max_x + 1):
            if (i, j) in tail_visited:
                if i == 0 and j == 0:
                    l += "s"
                else:
                    l += "#"
            else:
                l += "."
        print(l)


if __name__ == "__main__":
    movements = read("input/9.txt")
    pos_h = (0, 0)
    pos_t = (0, 0)
    tail_visited = {pos_t}
    for dir, steps in movements:
        for _ in range(steps):
            pos_h, pos_t = move(pos_h, pos_t, dir)
            tail_visited.add(pos_t)
    pretty_print(tail_visited)
    print(len(tail_visited))
