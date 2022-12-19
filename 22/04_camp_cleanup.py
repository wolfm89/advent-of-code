#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def read(filename):
    section_pairs = []
    with open(filename, "r") as reader:
        for line in reader:
            first, second = line.strip().split(",")
            section_pairs.append(([int(i) for i in first.split("-")], [int(i) for i in second.split("-")]))
    return section_pairs


def contains(first, second):
    return (first[0] >= second[0] and first[1] <= second[1]) or (first[0] <= second[0] and first[1] >= second[1])


def overlaps(first, second):
    return (
        (first[0] < second[0] and first[1] >= second[0] and first[1] < second[1])
        or (first[0] > second[0] and first[0] <= second[1] and first[1] > second[1])
        or (first[0] == second[0] and first[1] == second[1])
        or (first[0] >= second[0] and first[1] <= second[1])
        or (first[0] <= second[0] and first[1] >= second[1])
    )


if __name__ == "__main__":
    section_pairs = read("input/4.txt")
    print(sum([contains(first, second) for first, second in section_pairs]))
    print(sum([overlaps(first, second) for first, second in section_pairs]))
