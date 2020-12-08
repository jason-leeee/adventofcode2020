import os
import sys
import math
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def machine_exec(codes):
    size = len(codes)
    acc = 0
    pos = 0
    executed = {}
    terminated = False
    while pos not in executed:
        executed[pos] = True
        [opc, opr] = codes[pos].split(" ")
        opr = int(opr)
        if opc == "acc":
            acc += opr
            pos += 1
        elif opc == "jmp":
            pos += opr
        elif opc == "nop":
            pos += 1
        if pos >= size:
            terminated = True
            break
    return acc, terminated


def solution(lines):
    acc, _ = machine_exec(lines)
    return acc


def solution2(lines):
    for i, code in enumerate(lines):
        if code[:3] == "jmp":
            newcode = "nop" + code[3:]
        elif code[:3] == "nop":
            newcode = "jmp" + code[3:]
        else:
            continue
        lines[i] = newcode
        acc, terminated = machine_exec(lines)
        lines[i] = code
        if terminated:
            return acc
    return -1


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
