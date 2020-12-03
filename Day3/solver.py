import os
import sys
import math
import random
import itertools
import numpy as np


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


find_trees = lambda s, right, down: [s[row][(right * (step + 1)) % len(s[0])] for step, row in enumerate(range(down, len(s), down))].count("#")


def solution(lines):
    #return [s[i][(3 * i) % len(s[0])] for i in range(1, len(s))].count("#")
    return find_trees(lines, 3, 1)


def solution2(lines):
    prod = 1
    for right, down in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        print(find_trees(lines, right, down))
        prod *= find_trees(lines, right, down)
    return prod


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
