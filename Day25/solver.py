import os
import sys
import math
import copy
import itertools
import numpy as np


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def find_loop_size(snumber, targetkey):
    s = 1
    loopsize = 0
    while s != targetkey:
        s = s * snumber % 20201227
        loopsize += 1
    return loopsize


def encrypt_key(snumber, loopsize):
    s = 1
    while loopsize:
        loopsize -= 1
        s = s * snumber % 20201227
    return s


def solution(lines):
    snumber = 7
    cardkey = int(lines[0])
    doorkey = int(lines[1])
    cardls = find_loop_size(snumber, cardkey)
    doorls = find_loop_size(snumber, doorkey)
    print(f"card loop size: {cardls}")
    print(f"door loop size: {doorls}")
    return encrypt_key(cardkey, doorls)


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution(lines)
    print(f"answer: {ans}")
