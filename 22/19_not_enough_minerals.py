#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import math
from enum import Enum
from typing import NamedTuple
from collections import deque
from functools import cache


class Material(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


class Blueprint(NamedTuple):
    id: int
    robots: tuple[int]
    max_expenses: tuple[int]

    @cache
    def affordable_robot_types(self, inventory: tuple[int]) -> tuple[Material]:
        materials = tuple()
        for material in reversed(Material):
            if all(inventory[i] >= v for i, v in enumerate(self.robots[material.value])):
                materials += (material,)
        return materials


def read(filename: str) -> list[Blueprint]:
    with open(filename, "r") as reader:
        for line in reader:
            numbers = [int(s) for s in re.findall(r"\b\d+\b", line.strip())]
            robots = (
                (numbers[1], 0, 0, 0),
                (numbers[2], 0, 0, 0),
                (numbers[3], numbers[4], 0, 0),
                (numbers[5], 0, numbers[6], 0),
            )
            max_ore = max(robot[Material.ORE.value] for robot in robots)
            max_clay = numbers[4]
            max_obsidian = numbers[6]
            yield Blueprint(
                numbers[0],
                robots,
                (max_ore, max_clay, max_obsidian, math.inf),
            )


def bfs(blueprint: Blueprint, T: int, init_robots: tuple[int], init_inventory: tuple[int]) -> int:
    best_state = (None, None, (0,) * len(Material))
    queue = deque([(0, init_robots, init_inventory)])
    j = 0
    while queue:
        t, robots, inventory = queue.popleft()
        j += 1
        if j % 100000 == 0:
            print(best_state)
        affordable_robot_types = blueprint.affordable_robot_types(inventory)
        if Material.GEODE in affordable_robot_types:
            affordable_robot_types = (Material.GEODE,)
        for i, n in enumerate(robots):
            inventory = update(inventory, i, inventory[i] + n)
        if best_state[2][Material.GEODE.value] < inventory[Material.GEODE.value]:
            best_state = (t, robots, inventory)
        t += 1
        if t == T:
            continue
        if not Material.GEODE in affordable_robot_types:
            state = (t, robots, inventory)
            max_geodes = calc_max_geodes(T, *state)
            if max_geodes > best_state[2][Material.GEODE.value]:
                queue.append(state)
        for type in affordable_robot_types:
            if robots[type.value] >= blueprint.max_expenses[type.value]:
                continue
            robots = update(robots, type.value, robots[type.value] + 1)
            for i, n in enumerate(blueprint.robots[type.value]):
                inventory = update(inventory, i, inventory[i] - n)
            state = (t, robots, inventory)
            max_geodes = calc_max_geodes(T, *state)
            if max_geodes > best_state[2][Material.GEODE.value]:
                queue.append(state)
    print(best_state)
    return best_state[2][Material.GEODE.value]


def update(t: tuple, i: int, v):
    l = list(t)
    l[i] = v
    return tuple(l)


def calc_max_geodes(T, t, robots, inventory):
    t_rem = T - t
    return inventory[Material.GEODE.value] + t_rem * robots[Material.GEODE.value] + sum(range(t_rem + 1))


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
    robots: tuple[int] = (1, 0, 0, 0)
    inventory: tuple[int] = (0,) * len(Material)

    quality_levels = []
    for blueprint in blueprints:
        n_geodes = bfs(blueprint, T, robots, inventory)
        print(blueprint.id, n_geodes)
        quality_levels.append(blueprint.id * n_geodes)
    print(sum(quality_levels))
