#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from enum import Enum, auto
from typing import NamedTuple


class Material(Enum):
    ORE = auto()
    CLAY = auto()
    OBSIDIAN = auto()
    GEODE = auto()


class Robot(NamedTuple):
    type: Material
    requires: dict[Material, int]


class Blueprint(NamedTuple):
    id: int
    robots: list[Robot]


def read(filename):
    with open(filename, "r") as reader:
        for line in reader:
            numbers = [int(s) for s in re.findall(r"\b\d+\b", line.strip())]
            robots = [
                Robot(Material.ORE, {Material.ORE: numbers[1]}),
                Robot(Material.CLAY, {Material.ORE: numbers[2]}),
                Robot(Material.OBSIDIAN, {Material.ORE: numbers[3], Material.CLAY: numbers[4]}),
                Robot(Material.GEODE, {Material.ORE: numbers[5], Material.OBSIDIAN: numbers[6]}),
            ]
            yield Blueprint(numbers[0], robots)


if __name__ == "__main__":
    args = sys.argv[1:]
    test = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/19_test.txt")
    else:
        input = read("input/19.txt")

    blueprints = input

    for blueprint in blueprints:
        print(blueprint)
