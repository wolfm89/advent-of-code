#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == "__main__":
    calories = []
    with open("input/1.txt", "r") as reader:
        calorie = 0
        for line in reader:
            num = line.strip()
            if not num:
                calories.append(calorie)
                calorie = 0
                continue
            calorie += int(num)
    calories.sort(reverse=True)
    print(calories[0])
    print(sum(calories[:3]))
