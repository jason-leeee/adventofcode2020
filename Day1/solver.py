import os
import sys
import math
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def solution(lines):
    nums = list(map(int, lines))
    intmap = {x: i for i, x in enumerate(nums)}
    for i, x in enumerate(nums):
        y = 2020 - x
        if y in intmap and intmap[y] != i:
            print(x, y)
            return x * y
    return 0


def solution2(lines):
    nums = list(map(int, lines))
    intmap = {x: i for i, x in enumerate(nums)}
    for i, x in enumerate(nums[:-1]):
        for j, y in enumerate(nums[i + 1:]):
            z = 2020 - x - y
            if z in intmap and intmap[z] != i and intmap[z] != j:
                print(x, y, z)
                return x * y * z
    return 0


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
