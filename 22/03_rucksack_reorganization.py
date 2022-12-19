#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string


def read_contents_v1(filename):
    contents = []
    with open(filename, "r") as reader:
        for line in reader:
            line = line.strip()
            half = int(len(line) / 2)
            left = line[:half]
            right = line[half:]
            contents.append((left, right))
    return contents


def read_contents_v2(filename):
    contents = []
    with open(filename, "r") as reader:
        lines = reader.read().splitlines()
        for i in range(0, len(lines), 3):
            contents.append(lines[i : i + 3])
    return contents


if __name__ == "__main__":
    priorities = string.ascii_lowercase + string.ascii_uppercase
    contents = read_contents_v1("input/3.txt")
    print(sum(priorities.index(set(left).intersection(right).pop()) + 1 for left, right in contents))

    contents = read_contents_v2("input/3.txt")
    print(sum(priorities.index(set(r1).intersection(r2).intersection(r3).pop()) + 1 for r1, r2, r3 in contents))
