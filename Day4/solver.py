import os
import sys
import math
import random
import itertools
import numpy as np


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


REQUIRED_FIELDS = {
    "byr": lambda v: 1920 <= int(v) <= 2002,
    "iyr": lambda v: 2010 <= int(v) <= 2020,
    "eyr": lambda v: 2020 <= int(v) <= 2030,
    "hgt": lambda v: 150 <= int(v[:-2]) <= 193 if v.endswith("cm") else 59 <= int(v[:-2]) <= 76,
    "hcl": lambda v: v[0] == "#" and len(v) == 7 and sum([1 for c in v[1:] if c.isalnum()]) == 6,
    "ecl": lambda v: v in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
    "pid": lambda v: sum([1 for c in v if c.isnumeric()]) == 9,
    "cid": lambda _: True
}


def is_present(passport):
    bpresent = True
    for field in REQUIRED_FIELDS.keys():
        if field == "cid":
            continue
        if field + ":" not in passport:
            bpresent = False
            break
    return bpresent


def is_valid(passport):
    bvalid = True
    seps = passport.split(" ")
    for sep in seps:
        if not sep:
            continue
        [k, v] = sep.split(":")
        if not REQUIRED_FIELDS[k](v):
            bvalid = False
            break
    return bvalid


def solution(lines):
    passports = []
    s = ""
    for line in lines:
        if line:
            s += line + " "
        else:
            passports.append(s)
            s = ""
    passports.append(s)
    
    total_valid = 0
    for passport in passports:
        print(passport)
        if is_present(passport) and is_valid(passport):
            total_valid += 1

    return total_valid


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution(lines)
    print(f"answer: {ans}")
