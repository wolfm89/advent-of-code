#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import sys


class Snafu:
    BASE: int = 5
    numbers: list[int]

    def __init__(self, number: str) -> None:
        self.numbers = []
        for c in reversed(number):
            n = int(c) if c not in ("=", "-") else -1 if c == "-" else -2
            self.numbers.append(n)

    def __repr__(self) -> str:
        return "".join(str(n) if n not in (-1, -2) else "=" if n == -2 else "-" for n in reversed(self.numbers))

    def decimal(self) -> int:
        s = 0
        for i in range(len(self.numbers)):
            s += self.numbers[i] * self.BASE**i
        return s

    @classmethod
    def from_decimal(cls, number: int) -> Snafu:
        s = ""
        while number != 0:
            remainder = number % cls.BASE
            number //= cls.BASE
            s = str(remainder) + s
        snafu = ""
        add = 0
        for c in reversed(s):
            if add == 1:
                c = str(int(c) + 1)
                add = 0
            if c == "3":
                add = 1
                c = "="
            if c == "4":
                add = 1
                c = "-"
            if c == "5":
                add = 1
                c = "0"
            snafu += c
        return Snafu("".join(reversed(snafu)))


def read(filename: str) -> list[Snafu]:
    res = []
    with open(filename, "r") as reader:
        for line in reader:
            res.append(Snafu(line.strip()))
    return res


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    test: bool = False
    if len(args) > 0 and args[0] == "test":
        test = True

    if test:
        input = read("input/25_test.txt")
    else:
        input = read("input/25.txt")

    numbers = input

    s = sum(n.decimal() for n in numbers)
    print(Snafu.from_decimal(s))
