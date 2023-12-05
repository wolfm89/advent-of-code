#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# List of regex patterns for digits 0-9 and words one-nine
numbers = [
    r"\d",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def str_to_int(string):
    """
    Convert a string to an integer.
    If the string is a word, return the index of the word in the list of numbers.
    """
    try:
        return int(string)
    except ValueError:
        return numbers.index(string)


def get_calibration_value_part1(line):
    digits = re.findall(r"\d", line)
    first_digit = str_to_int(digits[0])
    last_digit = str_to_int(digits[-1])
    return first_digit * 10 + last_digit


def get_calibration_value_part2(line):
    """
    Get the calibration value of a line of text.
    The calibration value is the sum of the first and last digits in the line.
    For example, if the line is "one5two8three", the calibration value is 10 + 3 = 13.
    """
    # Lookahead: https://stackoverflow.com/a/11430936
    digits = re.findall(f"(?=({'|'.join(numbers)}))", line)
    first_digit = str_to_int(digits[0])
    last_digit = str_to_int(digits[-1])
    return first_digit * 10 + last_digit


if __name__ == "__main__":
    with open("input/data.txt", "r") as reader:
        sum_part1 = 0
        sum_part2 = 0
        for line in reader:
            calibration_value_part1 = get_calibration_value_part1(line.rstrip())
            calibration_value_part2 = get_calibration_value_part2(line.rstrip())
            sum_part1 += calibration_value_part1
            sum_part2 += calibration_value_part2
        print(sum_part1)
        print(sum_part2)
