#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from nis import maps


def get_interval(start, n):
    return start, start + n


if __name__ == "__main__":
    with open("input/test1.txt", "r") as reader:
        entities_part1 = [int(s) for s in reader.readline().split(":")[1].strip().split()]
        entities_part2 = [get_interval(s, n) for s, n in zip(entities_part1[::2], entities_part1[1::2])]
        reader.readline()

        maps_part1 = []
        while reader.readline():
            map_ = []
            while True:
                line = reader.readline().strip()
                if not line:
                    break
                map_.append([int(n) for n in line.split()])
            maps_part1.append(map_)
        maps_part2 = [
            [
                (
                    get_interval(interval[1], interval[2]),
                    get_interval(interval[0], interval[2]),
                )
                for interval in m
            ]
            for m in maps_part1
        ]
    # print(entities_part1)
    # print(maps_part1)
    print(entities_part2)
    print(maps_part2)

    for map_ in maps_part1:
        for i in range(len(entities_part1)):
            for interval in map_:
                if interval[1] <= entities_part1[i] < interval[1] + interval[2]:
                    entities_part1[i] = interval[0] + entities_part1[i] - interval[1]
                    break
    print(min(entities_part1))
