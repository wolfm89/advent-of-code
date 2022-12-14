#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
import math


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


def move(pos, dir, n=1):
    return (pos[0] + dir.value[0] * n, pos[1] + dir.value[1] * n)


def touches(p1, p2):
    if p1 == p2:
        return True
    l = norm(conn(p1, p2))
    return l == 1 or l == math.sqrt(2)


def conn(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])


def norm(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def normalize(vec):
    l = norm(vec)
    return (vec[0] / l, vec[1] / l)


def follow(pos_h, pos_t):
    if touches(pos_h, pos_t):
        return pos_t
    dir = normalize(conn(pos_h, pos_t))
    if dir in [d.value for d in Dir]:  # H and T on same row or column
        dir = Dir(dir)
        pos_t_new = move(pos_t, dir)
    else:
        dir = (math.copysign(1, dir[0]), math.copysign(1, dir[1]))
        pos_t_new = move(pos_t, Dir((dir[0], 0)))
        pos_t_new = move(pos_t_new, Dir((0, dir[1])))
    return pos_t_new


def pretty_print(positions):
    max_x = max(positions, key=lambda p: p[0])[0]
    min_x = min(positions, key=lambda p: p[0])[0]
    max_y = max(positions, key=lambda p: p[1])[1]
    min_y = min(positions, key=lambda p: p[1])[1]
    for j in range(max_y, min_y - 1, -1):
        l = ""
        for i in range(min_x, max_x + 1):
            if (i, j) in positions:
                if i == 0 and j == 0:
                    l += "s"
                else:
                    l += "#"
            else:
                l += "."
        print(l)


def visit(movements, n):
    positions = [(0, 0) for _ in range(n)]
    tail_visited = {(0, 0)}
    for dir, steps in movements:
        for _ in range(steps):
            positions[0] = move(positions[0], dir)
            for i in range(len(positions) - 1):
                positions[i + 1] = follow(positions[i], positions[i + 1])
            tail_visited.add(positions[-1])
    return tail_visited


if __name__ == "__main__":
    movements = read("input/9.txt")

    n = 2
    tail_visited = visit(movements, n)
    pretty_print(tail_visited)
    visit_count_a = len(tail_visited)

    n = 10
    tail_visited = visit(movements, n)
    pretty_print(tail_visited)
    visit_count_b = len(tail_visited)

    print(visit_count_a)
    print(visit_count_b)
