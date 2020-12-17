import os
import sys
import math
import random
import itertools
import numpy as np


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def init_dim_3d(lines):
    dim = {}
    z = 0
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            dim[(x, y, z)] = 1 if char == "#" else 0
    return dim


def get_neighbors_3d(dim, x, y, z):
    ofs = [
        (-1, -1, -1), (-1, -1, 0), (-1, -1, 1), (-1, 0, -1), (-1, 0, 0), (-1, 0, 1),
        (-1, 1, -1), (-1, 1, 0), (-1, 1, 1), (0, -1, -1), (0, -1, 0), (0, -1, 1),
        (0, 0, -1), (0, 0, 1), (0, 1, -1), (0, 1, 0), (0, 1, 1), (1, -1, -1),
        (1, -1, 0), (1, -1, 1), (1, 0, -1), (1, 0, 0), (1, 0, 1), (1, 1, -1),
        (1, 1, 0), (1, 1, 1)
    ]
    num_neighbors = 0
    for ox, oy, oz in ofs:
        if dim.get((x + ox, y + oy, z + oz), 0) == 1:
            num_neighbors += 1
    return num_neighbors


def solution(lines):
    dim = init_dim_3d(lines)

    MAX_CYCLE = 6
    INIT_D = len(lines)
    MAX_D = MAX_CYCLE

    for cycle in range(MAX_CYCLE):
        new_dim = {}
        for x in range(-MAX_D, INIT_D + MAX_D + 1):
            for y in range(-MAX_D, INIT_D + MAX_D + 1):
                for z in range(-MAX_D, INIT_D + MAX_D + 1):
                    num_neighbors = get_neighbors_3d(dim, x, y, z)
                    s = dim.get((x, y, z), 0)
                    if s == 1 and (num_neighbors == 2 or num_neighbors == 3):
                        new_dim[(x, y, z)] = 1
                    elif s == 0 and num_neighbors == 3:
                        new_dim[(x, y, z)] = 1
                    else:
                        new_dim[(x, y, z)] = 0
        dim = new_dim

    return sum(dim.values())


def init_dim_4d(lines):
    dim = {}
    z = 0
    w = 0
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            dim[(x, y, z, w)] = 1 if char == "#" else 0
    return dim


def get_neighbors_4d(dim, x, y, z, w):
    ofs = []
    ofs.extend([
        (-1, -1, -1, -1), (-1, -1, -1, 0), (-1, -1, -1, 1), (-1, -1, 0, -1), (-1, -1, 0, 0), (-1, -1, 0, 1),
        (-1, -1, 1, -1), (-1, -1, 1, 0), (-1, -1, 1, 1), (-1, 0, -1, -1), (-1, 0, -1, 0), (-1, 0, -1, 1),
        (-1, 0, 0, -1), (-1, 0, 0, 1), (-1, 0, 1, -1), (-1, 0, 1, 0), (-1, 0, 1, 1), (-1, 1, -1, -1),
        (-1, 1, -1, 0), (-1, 1, -1, 1), (-1, 1, 0, -1), (-1, 1, 0, 0), (-1, 1, 0, 1), (-1, 1, 1, -1),
        (-1, 1, 1, 0), (-1, 1, 1, 1), (-1, 0, 0, 0)
    ])
    ofs.extend([
        (0, -1, -1, -1), (0, -1, -1, 0), (0, -1, -1, 1), (0, -1, 0, -1), (0, -1, 0, 0), (0, -1, 0, 1),
        (0, -1, 1, -1), (0, -1, 1, 0), (0, -1, 1, 1), (0, 0, -1, -1), (0, 0, -1, 0), (0, 0, -1, 1),
        (0, 0, 0, -1), (0, 0, 0, 1), (0, 0, 1, -1), (0, 0, 1, 0), (0, 0, 1, 1), (0, 1, -1, -1),
        (0, 1, -1, 0), (0, 1, -1, 1), (0, 1, 0, -1), (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, -1),
        (0, 1, 1, 0), (0, 1, 1, 1)#, (0, 0, 0, 0)
    ])
    ofs.extend([
        (1, -1, -1, -1), (1, -1, -1, 0), (1, -1, -1, 1), (1, -1, 0, -1), (1, -1, 0, 0), (1, -1, 0, 1),
        (1, -1, 1, -1), (1, -1, 1, 0), (1, -1, 1, 1), (1, 0, -1, -1), (1, 0, -1, 0), (1, 0, -1, 1),
        (1, 0, 0, -1), (1, 0, 0, 1), (1, 0, 1, -1), (1, 0, 1, 0), (1, 0, 1, 1), (1, 1, -1, -1),
        (1, 1, -1, 0), (1, 1, -1, 1), (1, 1, 0, -1), (1, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, -1),
        (1, 1, 1, 0), (1, 1, 1, 1), (1, 0, 0, 0)
    ])
    num_neighbors = 0
    for ox, oy, oz, ow in ofs:
        if dim.get((x + ox, y + oy, z + oz, w + ow), 0) == 1:
            num_neighbors += 1
    return num_neighbors


def solution2(lines):
    dim = init_dim_4d(lines)

    MAX_CYCLE = 6
    INIT_D = len(lines)
    MAX_D = MAX_CYCLE

    for cycle in range(MAX_CYCLE):
        new_dim = {}
        for x in range(-MAX_D, INIT_D + MAX_D + 1):
            for y in range(-MAX_D, INIT_D + MAX_D + 1):
                for z in range(-MAX_D, INIT_D + MAX_D + 1):
                    for w in range(-MAX_D, INIT_D + MAX_D + 1):
                        num_neighbors = get_neighbors_4d(dim, x, y, z, w)
                        s = dim.get((x, y, z, w), 0)
                        if s == 1 and (num_neighbors == 2 or num_neighbors == 3):
                            new_dim[(x, y, z, w)] = 1
                        elif s == 0 and num_neighbors == 3:
                            new_dim[(x, y, z, w)] = 1
                        else:
                            new_dim[(x, y, z, w)] = 0
        dim = new_dim

    return sum(dim.values())


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
