#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import functools


def read(filename):
    with open(filename, "r") as reader:
        lines = [json.loads(l) for l in (line.strip() for line in reader) if l]
    return [(p, q) for p, q in zip(lines[::2], lines[1::2])]


def correct(p, q):
    if type(p) is int and type(q) is int:
        return 0 if p == q else -1 if p < q else 1
    elif type(p) is int:
        p = [p]
    elif type(q) is int:
        q = [q]
    else:
        return correctly_ordered_pair(p, q)
    return correct(p, q)


def correctly_ordered_pair(p, q):
    length = max(len(p), len(q))
    for i in range(length):
        if i == len(p):
            return -1
        if i == len(q):
            return 1
        res = correct(p[i], q[i])
        if res != 0:
            return res
    return 0


def correctly_ordered_pairs(pairs):
    correctly_ordered_indices = []
    for i, pair in enumerate(pairs, start=1):
        res = correctly_ordered_pair(pair[0], pair[1])
        if res == -1:
            correctly_ordered_indices.append(i)
    return correctly_ordered_indices


if __name__ == "__main__":
    pairs = read("input/13.txt")
    correctly_ordered_indices = correctly_ordered_pairs(pairs)
    print(sum(correctly_ordered_indices))

    signals = [s for p in pairs for s in p]
    divider_packet_1 = [[2]]
    divider_packet_2 = [[6]]
    signals.append(divider_packet_1)
    signals.append(divider_packet_2)

    signals.sort(key=functools.cmp_to_key(correctly_ordered_pair))
    print((signals.index(divider_packet_1) + 1) * (signals.index(divider_packet_2) + 1))
