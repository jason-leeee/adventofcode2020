import os
import sys
import math
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def solution(lines):
    nums = list(map(int, lines))

    N_PREV = 25

    for k, x in enumerate(nums[N_PREV:]):
        idx = N_PREV + k
        addups = []
        min_k = idx - N_PREV
        max_k = idx
        for i in range(min_k, max_k):
            for j in range(i + 1, max_k):
                addups.append(nums[i] + nums[j])
        if x not in addups:
            return x
    return -1


def solution2(lines):
    target = solution(lines)
    print(f"target: {target}")

    nums = list(map(int, lines))
    for n in range(2, len(lines)):
        for i in range(0, len(lines) - n):
            probes = nums[i:i + n]
            if sum(probes) == target:
                print(probes)
                return min(probes) + max(probes)


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
