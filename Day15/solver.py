import os
import sys
import math
import random
import itertools
import numpy as np


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def solution(lines):
    nums = list(map(int, lines[0].split(",")))

    nums_turn = {}
    nums_count = {}
    for i, k in enumerate(nums):
        nums_turn[k] = nums_turn.get(k, []) + [i + 1]

    prev = nums[-1]
    for turn in range(len(nums) + 1, 2021):
        if prev in nums_turn and len(nums_turn[prev]) >= 2:
            speak = nums_turn[speak][-1] - nums_turn[speak][-2]
        else:
            speak = 0
        print(f"turn: {turn}, speak: {speak}")
        nums_turn[speak] = nums_turn.get(speak, []) + [turn]
        prev = speak
        turn += 1

    return prev


def solution2(lines):
    nums = list(map(int, lines[0].split(",")))

    nums_turn = {}
    nums_count = {}
    for i, k in enumerate(nums):
        nums_turn[k] = nums_turn.get(k, []) + [i + 1]

    prev = nums[-1]
    for turn in range(len(nums) + 1, 30000001):
        if prev in nums_turn and len(nums_turn[prev]) >= 2:
            speak = nums_turn[speak][-1] - nums_turn[speak][-2]
        else:
            speak = 0
        if turn % 10000 == 0:
            print(f"turn: {turn}, speak: {speak}")
        
        nt = nums_turn.get(speak, [])
        nt.append(turn)
        if len(nt) > 2:
            nt = nt[-2:]
        nums_turn[speak] = nt
        
        prev = speak
        turn += 1

    return prev


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
