#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import Optional, Generator, Any
import operator
import re

OPS: dict[str, Any] = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
OPS_OPP: dict[Any, Any] = {
    operator.sub: operator.add,
    operator.add: operator.sub,
    operator.truediv: operator.mul,
    operator.mul: operator.truediv,
}


class Monkey:
    def __init__(
        self, name: str, deps: Optional[tuple[str, str]] = None, op: Optional[Any] = None, num: int = 0
    ) -> None:
        self.name: str = name
        self.deps: Optional[tuple[str, str]] = deps
        self.op: Optional[Any] = op
        self.num: int = num

    def __str__(self) -> str:
        if self.deps:
            op: str = next(key for key, value in OPS.items() if value == self.op)
            return f"{self.name}: {self.deps[0]} {op} {self.deps[1]}"
        else:
            return f"{self.name}: {self.num}"


def read(filename: str) -> Generator[tuple[str, Monkey], None, None]:
    with open(filename, "r") as reader:
        for line in reader:
            res = re.search(r"([a-z]{4}): (\d+)", line.strip())
            if res is not None:
                yield res.group(1), Monkey(res.group(1), num=int(res.group(2)))
            else:
                res = re.search(r"([a-z]{4}): ([a-z]{4}) (.) ([a-z]{4})", line.strip())
                yield res.group(1), Monkey(res.group(1), deps=(res.group(2), res.group(4)), op=OPS[res.group(3)])


def calc(monkeys: dict[str, Monkey], m: Monkey) -> int:
    if m.deps:
        return int(m.op(calc(monkeys, monkeys[m.deps[0]]), calc(monkeys, monkeys[m.deps[1]])))
    else:
        return m.num


def find_monkey_branches_with_and_without(monkeys: dict[str, Monkey], root: str, curr: str) -> tuple[str, str]:
    while curr not in monkeys[root].deps:
        for m in monkeys.values():
            if m.deps and curr in m.deps:
                curr = m.name
                break
    return curr, next(name for name in monkeys[root].deps if name != curr)


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    test: bool = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/21_test.txt")
    else:
        input = read("input/21.txt")

    monkeys: dict[str, Monkey] = dict(input)
    print(calc(monkeys, monkeys["root"]))

    root = "root"
    me = "humn"

    x = None
    while root != me:
        m_with, m_without = find_monkey_branches_with_and_without(monkeys, root, me)
        rhs = True if monkeys[root].deps.index(m_without) == 1 else False
        other_branch_value = calc(monkeys, monkeys[m_without])
        if x is not None:
            if rhs or monkeys[root].op in (operator.add, operator.mul):
                x = int(OPS_OPP[monkeys[root].op](x, other_branch_value))
            else:
                x = int(monkeys[root].op(other_branch_value, x))
        else:
            x = other_branch_value
        root = m_with
    print(x)
