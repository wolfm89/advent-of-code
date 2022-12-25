#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from collections import deque


def read(filename):
    valves = {}
    with open(filename, "r") as reader:
        for line in reader:
            result = re.search(r"Valve ([A-Z][A-Z]).*=(\d+);.*valves? (.*$)", line.strip())
            valves[result.group(1)] = {"flow_rate": int(result.group(2)), "connections": result.group(3).split(", ")}
    return valves


def bfs(valves, T, pos):
    # time left, current position, valves open, total pressure released
    queue = deque([(T, pos, [], 0)])

    processed = set()
    released_pressures = []

    while queue:
        t, p, o, pr = queue.popleft()

        if t == 0:
            released_pressures.append(pr)
            continue

        if (p, tuple(o)) in processed:
            continue
        processed.add((p, tuple(o)))

        for v in o:
            pr += valves[v]["flow_rate"]

        for c in valves[p]["connections"]:
            queue.append((t - 1, c, o, pr))
        if valves[p]["flow_rate"] > 0 and p not in o:
            queue.append((t - 1, p, o + [p], pr))

    return max(released_pressures)


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
    print(bfs(valves, T, pos))
