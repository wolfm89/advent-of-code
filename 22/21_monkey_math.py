#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import Optional, Generator, Any
import operator
import re

OPS: dict[str, Any] = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


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
