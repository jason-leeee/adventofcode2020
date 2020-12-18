import os
import sys
import math
import random
import itertools
import numpy as np


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def exp_construct(expstr, idx=0):
    oprs = []
    while idx < len(expstr):
        c = expstr[idx]
        if c == "(":
            suboprs, newidx = exp_construct(expstr, idx + 1)
            oprs.append(suboprs)
            idx = newidx
        elif c == ")":
            return oprs, idx + 1
        elif c == " ":
            idx += 1
        else:
            oprs.append(c)
            idx += 1
    return oprs, len(expstr)


def exp_add_precedence(exp):
    newexp = []
    i = 0
    while i < len(exp):
        x = exp[i]
        if isinstance(x, list):
            newexp.append(exp_add_precedence(x))
            i += 1
        else:
            if x == "+":
                lastop = newexp[-1]
                nextop = exp[i + 1]
                if isinstance(nextop, list):
                    nextop = exp_add_precedence(nextop)
                newexp[-1] = [lastop, "+", nextop]
                i += 2
            else:
                newexp.append(x)
                i += 1
    return newexp


def eval_exp(exp):
    s = exp[0]
    if isinstance(s, list):
        s = eval_exp(s)
    s = int(s)

    for i in range(1, len(exp), 2):
        opr = exp[i]
        num = exp[i + 1]
        if isinstance(num, list):
            num = eval_exp(num)
        num = int(num)
        if opr == "+":
            s += num
        elif opr == "*":
            s *= num

    return s


def eval_exp_string(expstr):
    print(f"expstr: {expstr}")
    oprs, _ = exp_construct(expstr, 0)
    print(f"oprs: {oprs}")

    return eval_exp(oprs)


def solution(lines):
    ans = 0
    for i, expstr in enumerate(lines):
        exp, _ = exp_construct(expstr, 0)
        print(f"[{i + 1}] exp: {exp}")
        ans += eval_exp(exp)
    return ans


def solution2(lines):
    ans = 0
    for i, expstr in enumerate(lines):
        print(f"[{i + 1}] exp:")
        exp, _ = exp_construct(expstr, 0)
        print(f"\tbefore: {exp}")
        exp = exp_add_precedence(exp)
        print(f"\tafter : {exp}")
        ans += eval_exp(exp)
    return ans


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
