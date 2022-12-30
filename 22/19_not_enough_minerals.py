#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import math
from enum import Enum, auto
from typing import NamedTuple, Optional
from collections import deque
from copy import copy


class Material(Enum):
    GEODE = auto()
    OBSIDIAN = auto()
    CLAY = auto()
    ORE = auto()


class Robot(NamedTuple):
    requires: dict[Material, int]


class Blueprint(NamedTuple):
    id: int
    robots: dict[Material, Robot]
    max_expenses: dict[Material, int]

    def affordable_robot_types(self, inventory: dict[Material, int], max_n: int = -1) -> list[Material]:
        materials = []
        for material in Material:
            if all(inventory[k] >= v for k, v in self.robots[material].requires.items()):
                materials.append(material)
                if max_n != -1 and len(materials) == max_n:
                    return materials
        return materials


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
            max_ore = max(robot.requires[Material.ORE] for robot in robots.values())
            max_clay = numbers[4]
            max_obsidian = numbers[6]
            yield Blueprint(
                numbers[0],
                robots,
                {
                    Material.ORE: max_ore,
                    Material.CLAY: max_clay,
                    Material.OBSIDIAN: max_obsidian,
                    Material.GEODE: math.inf,
                },
            )


def bfs(
    blueprint: Blueprint, T: int, init_robots: dict[Material, int], init_inventory: dict[Material, int]
) -> list[int]:
    queue = deque([(0, init_robots, init_inventory)])
    # i = 0
    while queue:
        t, robots, inventory = queue.popleft()
        # i += 1
        # if i % 10000 == 0:
        #     print(len(queue), t, robots, inventory)
        affordable_robot_types = blueprint.affordable_robot_types(inventory, max_n=2)
        for material, n in robots.items():
            inventory[material] += n
        t += 1
        if t == T:
            # if inventory[Material.GEODE] == 12:
            #     print(t, robots, inventory)
            yield inventory[Material.GEODE]
            continue
        if not Material.GEODE in affordable_robot_types:
            queue.append((t, copy(robots), copy(inventory)))
        for type in affordable_robot_types:
            if robots[type] >= blueprint.max_expenses[type]:
                continue
            new_robots = copy(robots)
            new_robots[type] += 1
            new_inventory = copy(inventory)
            for material, n in blueprint.robots[type].requires.items():
                new_inventory[material] -= n
            queue.append((t, new_robots, new_inventory))


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

    quality_levels = []
    for blueprint in blueprints:
        n_geodes = max(bfs(blueprint, T, copy(robots), copy(inventory)))
        print(blueprint.id, n_geodes)
        quality_levels.append(blueprint.id * n_geodes)
    print(sum(quality_levels))
