import os
import sys
import math
import copy
import itertools
import numpy as np


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def get_init_grid(grid, lines):
    y0 = grid.shape[0] // 2
    x0 = grid.shape[1] // 2
    for line in lines:
        y, x = y0, x0
        while line:
            if line[0] == "w":
                x -= 1
                lc = 1
            elif line[0] == "e":
                x += 1
                lc = 1
            elif line[:2] == "nw":
                x -= 1
                y -= 1
                lc = 2
            elif line[:2] == "ne":
                y -= 1
                lc = 2
            elif line[:2] == "sw":
                y += 1
                lc = 2
            elif line[:2] == "se":
                x += 1
                y += 1
                lc = 2
            line = line[lc:]
        grid[y][x] = 1 - grid[y][x]


def solution(lines):
    grid = np.zeros((100, 100), dtype=np.uint8)   # 0: white, 1: black
    get_init_grid(grid, lines)
    return np.count_nonzero(grid)


def get_neighbors(grid, y, x):
    n_white = 0
    n_black = 0
    neighbors = [(y, x - 1), (y, x + 1), (y - 1, x - 1), (y - 1, x), (y + 1, x), (y + 1, x + 1)]
    for ny, nx in neighbors:
        if grid[ny][nx] == 0:
            n_white += 1
        else:
            n_black += 1
    return n_white, n_black


def solution2(lines):
    # grid has to be big enough, otherwise the results are not correct
    grid = np.zeros((200, 200), dtype=np.uint8)   # 0: white, 1: black
    get_init_grid(grid, lines)
    for day in range(1, 101):
        newgrid = np.copy(grid)
        for y, row in enumerate(grid):
            for x, tile in enumerate(row):
                if not (1 <= y <= grid.shape[0] - 2): continue
                if not (1 <= x <= grid.shape[1] - 2): continue
                n_white, n_black = get_neighbors(grid, y, x)
                if tile == 0:   # white tile
                    if n_black == 2:
                        newgrid[y][x] = 1
                elif tile == 1:   # black tile
                    if n_black == 0 or n_black > 2:
                        newgrid[y][x] = 0
        grid = newgrid
        print(f"day {day} black tiles: {np.count_nonzero(grid)}")
    return np.count_nonzero(grid)


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
