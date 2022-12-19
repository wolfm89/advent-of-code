#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce  # forward compatibility for Python 3
import operator
import json


def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value


def read(filename):
    filetree = {}
    cur_path = []
    with open(filename, "r") as reader:
        if not reader.readline().strip() == "$ cd /":
            raise ValueError
        line = reader.readline().strip()
        while line:
            if line.startswith("$"):
                cmds = line.split(" ")[1:]
                if cmds[0] == "ls":
                    line = reader.readline().strip()
                    while line and not line.startswith("$"):
                        if line[0].isdigit():
                            size, fname = line.split(" ")
                            set_by_path(filetree, cur_path + [fname], int(size))
                        line = reader.readline().strip()
                elif cmds[0] == "cd":
                    if cmds[1] == "..":
                        cur_path.pop()
                    else:
                        cur_path.append(cmds[1])
                        set_by_path(filetree, cur_path, {})
                    line = reader.readline().strip()
    return filetree


def get_dir_size(dir):
    return sum([v if isinstance(v, int) else get_dir_size(v) for v in dir.values()])


def get_sizes(filetree, sizes):
    for k, v in filetree.items():
        if isinstance(v, dict):
            sizes.append((k, get_dir_size(v)))
            get_sizes(v, sizes)


if __name__ == "__main__":
    filetree = read("input/7.txt")
    print(json.dumps(filetree, indent=2))
    sizes = []
    get_sizes(filetree, sizes)
    sizes.sort(key=lambda s: s[1])
    print(sizes)
    used_space = get_dir_size(filetree)
    total_space = 70000000
    needed_space = 30000000
    space_to_free_up = needed_space - (total_space - used_space)
    print(sum([s for d, s in sizes if s <= 100000]))
    print([s for d, s in sizes if s >= space_to_free_up][0])
