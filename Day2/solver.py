import os
import sys
import math
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def solution(lines):
    total_valid = 0
    for line in lines:
        seps = line.split(" ")
        lens = seps[0].split("-")
        min_len = int(lens[0])
        max_len = int(lens[1])
        char = seps[1][0]
        password = seps[2]
        num_chars = len([x for x in password if x == char])
        if min_len <= num_chars <= max_len:
            total_valid += 1
    return total_valid


def solution2(lines):
    total_valid = 0
    for line in lines:
        seps = line.split(" ")
        pos = seps[0].split("-")
        pos1 = int(pos[0]) - 1
        pos2 = int(pos[1]) - 1
        char = seps[1][0]
        password = seps[2]
        if (password[pos1] == char and password[pos2] != char) or (password[pos1] != char and password[pos2] == char):
            total_valid += 1
    return total_valid


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
