#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def read(filename):
    with open(filename, "r") as reader:
        lines = [json.loads(l) for l in (line.strip() for line in reader) if l]
    return [(p, q) for p, q in zip(lines[::2], lines[1::2])]


def correct(p, q):
    if type(p) is int and type(q) is int:
        return -1 if p == q else p < q
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
            return True
        if i == len(q):
            return False
        res = correct(p[i], q[i])
        if not res:
            return False
        elif res == 1:
            return True
    return -1


def correctly_ordered_pairs(pairs):
    correctly_ordered_indices = []
    for i, pair in enumerate(pairs, start=1):
        res = correctly_ordered_pair(pair[0], pair[1])
        if res and res != -1:
            correctly_ordered_indices.append(i)
    return correctly_ordered_indices


if __name__ == "__main__":
    pairs = read("input/13.txt")
    correctly_ordered_indices = correctly_ordered_pairs(pairs)
    print(sum(correctly_ordered_indices))
