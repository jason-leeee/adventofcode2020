import os
import sys
import math
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def solution(lines):
    total_mass = 0
    for mass in lines:
        mass = int(mass) // 3 - 2
        total_mass += mass
    return total_mass


def solution2(lines):
    total_mass = 0
    for mass in lines:
        mass = int(mass)
        while mass > 0:
            mass = mass // 3 - 2
            if mass > 0:
                total_mass += mass
    return total_mass


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
