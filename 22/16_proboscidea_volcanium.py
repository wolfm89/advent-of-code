#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from copy import copy
from collections import deque
from collections import defaultdict


def read(filename):
    valves = {}
    with open(filename, "r") as reader:
        for line in reader:
            result = re.search(r"Valve ([A-Z][A-Z]).*=(\d+);.*valves? (.*$)", line.strip())
            valves[result.group(1)] = {"flow_rate": int(result.group(2)), "connections": result.group(3).split(", ")}
    return valves


def bfs(valves, T, pos):
    queue = deque([(T, pos, [], defaultdict(lambda: 0))])

    processed = set()
    solutions = []

    while queue:
        t, p, o, pr = queue.popleft()

        if t == 0:
            solutions.append((o, pr))
            continue

        if (p, tuple(o)) in processed:
            continue
        processed.add((p, tuple(o)))

        for v in o:
            pr[v] += valves[v]["flow_rate"]

        for c in valves[p]["connections"]:
            queue.append((t - 1, c, o, copy(pr)))
        if valves[p]["flow_rate"] > 0 and p not in o:
            queue.append((t - 1, p, o + [p], copy(pr)))

    return solutions


def create_range(n):
    result = []
    for i in range(n + 1):
        result.append(i)
        result.append(i)
    return result


def intersect(p, q):
    return any(i in p for i in q)


def intersect2(p, q):
    return not set(p).isdisjoint(q)


if __name__ == "__main__":
    args = sys.argv[1:]
    test = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        valves = read("input/16_test.txt")
    else:
        valves = read("input/16.txt")

    pos = "AA"
    T = 30

    solutions = bfs(valves, T, pos)
    best_solution = max(solutions, key=lambda x: sum(x[1].values()))
    print(best_solution)
    print(sum(best_solution[1].values()))

    T = 26
    solutions = bfs(valves, T, pos)
    solutions.sort(reverse=True, key=lambda x: sum(x[1].values()))

    best = None
    for s1 in solutions:
        for s2 in solutions:
            if not intersect(s1[0], s2[0]):
                sum1 = sum(s1[1].values())
                sum2 = sum(s2[1].values())
                if best is not None and sum2 < sum(best[1][1].values()):
                    break
                if best is None or (sum1 + sum2 > sum(best[0][1].values()) + sum(best[1][1].values())):
                    best = (s1, s2)
                    # print(best)
                    # print(sum(best[0][1].values()) + sum(best[1][1].values()))
    print(best)
    print(sum(best[0][1].values()) + sum(best[1][1].values()))
