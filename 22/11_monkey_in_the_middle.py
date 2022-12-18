#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
import math
from copy import deepcopy


def read_monkey(reader):
    line = reader.readline()
    line = reader.readline().strip()
    starting_items = [int(s.strip()) for s in line.split(":")[1].split(",")]
    line = reader.readline().strip()
    operation = line.split(" ")[-2:]
    if operation[0] == "+":
        operation[0] = operator.add
    elif operation[0] == "*" and operation[1] == "old":
        operation[0] = operator.pow
        operation[1] = 2
    elif operation[0] == "*":
        operation[0] = operator.mul
    operation[1] = int(operation[1])
    line = reader.readline().strip()
    test = int(line.split(" ")[-1])
    line = reader.readline().strip()
    target_true = int(line.split(" ")[-1])
    line = reader.readline().strip()
    target_false = int(line.split(" ")[-1])
    monkey = {
        "items": starting_items,
        "operation": operation,
        "test": [operator.mod, test, 0],
        "targets": [target_true, target_false],
        "n_items_inspected": 0,
    }
    return monkey


def read(filename):
    monkeys = []
    with open(filename, "r") as reader:
        while True:
            monkeys.append(read_monkey(reader))
            line = reader.readline()
            if not line:
                break
    return monkeys


def inspect_items(monkey, lcm=0):
    items = []
    targets = []
    for i in reversed(range(len(monkey["items"]))):
        monkey["items"][i] = monkey["operation"][0](monkey["items"][i], monkey["operation"][1])
        if lcm == 0:
            monkey["items"][i] //= 3
        else:
            monkey["items"][i] %= lcm
        if monkey["test"][0](monkey["items"][i], monkey["test"][1]) == monkey["test"][2]:
            targets.append(monkey["targets"][0])
        else:
            targets.append(monkey["targets"][1])
        items.append(monkey["items"].pop(i))
        monkey["n_items_inspected"] += 1
    return items, targets


def play_rounds(rounds, monkeys, lcm=0):
    for _ in range(rounds):
        for monkey in monkeys:
            items, targets = inspect_items(monkey, lcm)
            for item, target in zip(items, targets):
                monkeys[target]["items"].append(item)


if __name__ == "__main__":

    monkeys = read("input/11.txt")
    monkeys_norelief = deepcopy(monkeys)

    rounds = 20
    play_rounds(rounds, monkeys)
    for i, monkey in enumerate(monkeys):
        print(f"Monkey {i}: {', '.join(map(str, monkey['items']))}")
    print()
    for i, monkey in enumerate(monkeys):
        print(f"Monkey {i} inspected items {monkey['n_items_inspected']} times.")
    print(math.prod(sorted(m["n_items_inspected"] for m in monkeys)[-2:]))

    print()
    print()

    rounds = 10000
    divisors = [monkey["test"][1] for monkey in monkeys]
    lcm = math.lcm(*divisors)
    play_rounds(rounds, monkeys_norelief, lcm=lcm)
    for i, monkey in enumerate(monkeys_norelief):
        print(f"Monkey {i}: {', '.join(map(str, monkey['items']))}")
    print()
    for i, monkey in enumerate(monkeys_norelief):
        print(f"Monkey {i} inspected items {monkey['n_items_inspected']} times.")
    print(math.prod(sorted(m["n_items_inspected"] for m in monkeys_norelief)[-2:]))
