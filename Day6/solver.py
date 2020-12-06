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
    groups = []
    s = ""
    for line in lines:
        if line:
            s += line
        else:
            groups.append(set(s))
            s = ""
    groups.append(set(s))
    
    total_valid = 0
    for group in groups:
        total_valid += len(group)

    return total_valid


def common_elements(list1, list2):
    return "".join([element for element in list1 if element in list2])


def solution2(lines):
    groups = []
    restart = True
    s = ""
    for line in lines:
        if line:
            s = common_elements(s, line) if not restart else line
            restart = False
        else:
            groups.append(s)
            restart = True
            s = ""
    groups.append(s)
    
    total_valid = 0
    for group in groups:
        print(group)
        total_valid += len(group)

    return total_valid


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
