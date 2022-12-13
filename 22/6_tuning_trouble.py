#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def unique(s):
    return len(s) == len(set(s))


def first_unique_occ(s, wl):
    for i in range(len(s) - wl + 1):
        if unique(s[i : i + wl]):
            return s[i : i + wl], i + wl


if __name__ == "__main__":
    s = ""
    with open("input/6.txt", "r") as reader:
        s = reader.readline()
    print(first_unique_occ(s, 4))
    print(first_unique_occ(s, 14))
