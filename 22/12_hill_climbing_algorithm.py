#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import math


def altitude(c):
    return ord(c) - ord("a")


def find_and_replace(line, f, r):
    try:
        j = line.index(f)
        line[j] = r
        return j
    except ValueError:
        return None


def read(filename):
    S = altitude("S")
    E = altitude("E")

    start = (None, None)
    end = (None, None)
    elevation_map = []

    with open(filename, "r") as reader:
        for i, line in enumerate(reader):
            elevation_map.append([altitude(c) for c in line.strip()])
            if start[1] is None:
                start = (i, find_and_replace(elevation_map[-1], S, altitude("a")))
            if end[1] is None:
                end = (i, find_and_replace(elevation_map[-1], E, altitude("z")))
    return elevation_map, start, end


def init(elevation_map, start):
    unvisited = list(itertools.product(range(len(elevation_map)), range(len(elevation_map[0]))))
    distances = [[math.inf] * len(elevation_map[0]) for _ in range(len(elevation_map))]
    distances[start[0]][start[1]] = 0
    return unvisited, distances


def filter_max(neighbors, max_x, max_y):
    return [n for n in neighbors if n[1] < max_x and n[0] < max_y and n[0] >= 0 and n[1] >= 0]


def neighbors(p, max_x, max_y):
    return filter_max([(p[0] + 1, p[1]), (p[0], p[1] + 1), (p[0] - 1, p[1]), (p[0], p[1] - 1)], max_x, max_y)


def alt_diff(elevation_map, x, y):
    return elevation_map[x[0]][x[1]] - elevation_map[y[0]][y[1]]


def dijkstra(elevation_map, start, end):
    max_x = len(elevation_map[0])
    max_y = len(elevation_map)
    unvisited, distances = init(elevation_map, start)
    cur = start

    while True:
        unvisited_neighbors = [n for n in neighbors(cur, max_x, max_y) if n in unvisited]
        unvisited_neighbor_distances = [
            1 if alt_diff(elevation_map, n, cur) <= 1 else math.inf for n in unvisited_neighbors
        ]
        for n, d in zip(unvisited_neighbors, unvisited_neighbor_distances):
            d_full = distances[cur[0]][cur[1]] + d
            if distances[n[0]][n[1]] > d_full:
                distances[n[0]][n[1]] = d_full
        unvisited.remove(cur)
        if cur == end:
            return distances[end[0]][end[1]]
        else:
            unvisited_distances = [distances[i][j] for i, j in unvisited]
            m = min(unvisited_distances)
            if m == math.inf:
                return math.inf
            min_idx = unvisited_distances.index(m)
            cur = unvisited[min_idx]


def find_all(elevation_map, altitude):
    points = []
    for i, j in list(itertools.product(range(len(elevation_map)), range(len(elevation_map[0])))):
        if elevation_map[i][j] == altitude:
            points.append((i, j))
    return points


def dist(x, y):
    return math.sqrt((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2)


if __name__ == "__main__":
    elevation_map, start, end = read("input/12.txt")

    distance = dijkstra(elevation_map, start, end)
    print(distance)

    lowest_points = find_all(elevation_map, 0)
    lowest_points.sort(key=lambda p: dist(end, p))

    distances = [dijkstra(elevation_map, s, end) for s in lowest_points]
    print(min(distances))
