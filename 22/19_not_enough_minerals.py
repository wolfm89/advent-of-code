#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from enum import Enum, auto
from typing import NamedTuple, Optional
from collections import deque
from copy import copy


class Material(Enum):
    ORE = auto()
    CLAY = auto()
    OBSIDIAN = auto()
    GEODE = auto()


class Robot(NamedTuple):
    requires: dict[Material, int]


class Blueprint(NamedTuple):
    id: int
    robots: dict[Material, Robot]

    def affordable_robot_types(self, inventory: dict[Material, int]) -> list[Material]:
        for material in reversed(Material):
            if all(inventory[k] >= v for k, v in self.robots[material].requires.items()):
                yield material


def read(filename: str) -> list[Blueprint]:
    with open(filename, "r") as reader:
        for line in reader:
            numbers = [int(s) for s in re.findall(r"\b\d+\b", line.strip())]
            robots = {
                Material.ORE: Robot({Material.ORE: numbers[1]}),
                Material.CLAY: Robot({Material.ORE: numbers[2]}),
                Material.OBSIDIAN: Robot({Material.ORE: numbers[3], Material.CLAY: numbers[4]}),
                Material.GEODE: Robot({Material.ORE: numbers[5], Material.OBSIDIAN: numbers[6]}),
            }
            yield Blueprint(numbers[0], robots)


def bfs(
    blueprint: Blueprint, T: int, init_robots: dict[Material, int], init_inventory: dict[Material, int]
) -> list[int]:
    queue = deque([(T, init_robots, init_inventory)])
    i = 0
    while queue:
        t, robots, inventory = queue.popleft()
        i += 1
        if i % 10000 == 0:
            print(t, robots, inventory)
        affordable_robot_types = list(blueprint.affordable_robot_types(inventory))[:2]
        for material, n in robots.items():
            inventory[material] += n
        t -= 1
        if t == 0:
            yield inventory[Material.GEODE]
            continue
        # if not affordable_robot_types:
        queue.append((t, copy(robots), copy(inventory)))
        for type in affordable_robot_types:
            new_robots = copy(robots)
            new_robots[type] += 1
            new_inventory = copy(inventory)
            for material, n in blueprint.robots[type].requires.items():
                new_inventory[material] -= n
            queue.append((t, new_robots, copy(new_inventory)))


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    test: bool = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/19_test.txt")
    else:
        input = read("input/19.txt")

    blueprints: list[Blueprint] = list(input)

    T: int = 24
    robots: dict[Material, int] = {material: 0 for material in Material}
    robots[Material.ORE] += 1
    inventory: dict[Material, int] = {material: 0 for material in Material}

    for blueprint in blueprints[:1]:
        n_geodes = max(bfs(blueprint, T, robots, inventory))
        print(blueprint.id, n_geodes)
