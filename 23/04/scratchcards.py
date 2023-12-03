#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Set

# A dataclass that stores a card's information:
# the winning numbers, the player's numbers, matching numbers, and the number of copies of the card
@dataclass
class Card:
    winning_numbers: Set[int]
    my_numbers: Set[int]
    matches: Set[int]
    copies: int = 1


if __name__ == "__main__":
    with open("input/data.txt", "r") as reader:
        cards = []
        total_points_part1 = 0
        for line in reader:
            winning_numbers, my_numbers = line.split(":")[1].strip().split("|")
            winning_numbers = set(int(n) for n in winning_numbers.split())
            my_numbers = set(int(n) for n in my_numbers.split())
            matching_numbers = winning_numbers.intersection(my_numbers)

            # Part 1
            points_part1 = 2 ** (len(matching_numbers) - 1) if matching_numbers else 0
            total_points_part1 += points_part1

            # Part 2
            cards.append(Card(winning_numbers, my_numbers, matching_numbers))
        # Part 1
        print(total_points_part1)

        # Part 2
        for i, card in enumerate(cards):
            for _ in range(card.copies):
                if not card.matches:
                    continue
                for other_card in cards[i + 1 : i + 1 + len(card.matches)]:
                    other_card.copies += 1
        print(sum(c.copies for c in cards))
