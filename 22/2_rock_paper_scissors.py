#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class Shape(Enum):
    ROCK = (1, "SCISSORS", "PAPER")
    PAPER = (2, "ROCK", "SCISSORS")
    SCISSORS = (3, "PAPER", "ROCK")

    def __init__(self, score, wins_against, loses_against):
        self.score = score
        self.wins_against = wins_against
        self.loses_against = loses_against

    def against(self, shape):
        if shape.name == self.wins_against:
            return 6
        if shape.name == self.name:
            return 3
        return 0

    @classmethod
    def from_char(cls, char):
        if char in ("A", "X"):
            return cls.ROCK
        if char in ("B", "Y"):
            return cls.PAPER
        if char in ("C", "Z"):
            return cls.SCISSORS
        raise ValueError()

    @classmethod
    def from_result(cls, char, opp):
        if char == "X":
            return cls[cls.from_char(opp).wins_against]
        if char == "Y":
            return cls.from_char(opp)
        if char == "Z":
            return cls[cls.from_char(opp).loses_against]
        raise ValueError()


def read_games(filename, version=1):
    games = []
    with open(filename, "r") as reader:
        for line in reader:
            p1, p2 = line.strip().split(" ")
            if version == 1:
                games.append([Shape.from_char(p1), Shape.from_char(p2)])
            else:
                games.append([Shape.from_char(p1), Shape.from_result(p2, p1)])
    return games


def play(games):
    total_score = 0
    for game in games:
        # print(game[0].name, game[1].name, game[1].score, game[1].against(game[0]))
        total_score += game[1].score + game[1].against(game[0])
    return total_score


if __name__ == "__main__":
    games = read_games("input/2.txt")
    total_score = play(games)
    print(total_score)

    games = read_games("input/2.txt", version=2)
    total_score = play(games)
    print(total_score)
