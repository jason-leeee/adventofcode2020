import os
import sys
import math
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def decode_pass(bpass):
    srow = bpass[:7]
    srow = srow.replace("F", "0")
    srow = srow.replace("B", "1")
    row = int(srow, 2)

    scol = bpass[7:]
    scol = scol.replace("L", "0")
    scol = scol.replace("R", "1")
    col = int(scol, 2)

    return row, col


def solution(lines):
    m = 0
    for line in lines:
        row, col = decode_pass(line)
        sid = row * 8 + col
        print(sid)
        m = max(m, sid)
    return m


def solution2(lines):
    ids = {}
    for line in lines:
        row, col = decode_pass(line)
        sid = row * 8 + col
        ids[sid] = True

    print(sorted(ids.keys()))

    for x in range(min(ids.keys()) + 1, max(ids.keys())):
        if x not in ids and x - 1 in ids and x + 1 in ids:
            return x
    return 0


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
