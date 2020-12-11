import os
import sys
import math
import copy
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def get_adjacent(grid, x, y):
    h = len(grid)
    w = len(grid[0])

    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    num_adjacents = 0
    for y_offset, x_offset in offsets:
        yy = y + y_offset
        xx = x + x_offset
        if 0 <= yy < h and 0 <= xx < w:
            if grid[yy][xx] == "#":
                num_adjacents += 1
    return num_adjacents


def get_adjacent2(grid, x, y):
    h = len(grid)
    w = len(grid[0])

    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    num_adjacents = 0
    for y_offset, x_offset in offsets:
        yy = y
        xx = x
        while True:
            yy += y_offset
            xx += x_offset
            if 0 <= yy < h and 0 <= xx < w:
                if grid[yy][xx] == "#":
                    num_adjacents += 1
                    break
                elif grid[yy][xx] == "L":
                    break
            else:
                break
    return num_adjacents


def solution(grid):
    changed = False
    while True:
        newgrid = copy.deepcopy(grid)
        changed = False
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == "L" and get_adjacent(grid, x, y) == 0:
                    newgrid[y][x] = "#"
                    changed = True
                elif grid[y][x] == "#" and get_adjacent(grid, x, y) >= 4:
                    newgrid[y][x] = "L"
                    changed = True
        grid = newgrid
        if not changed:
            break

    num_occupied = 0
    for row in grid:
        for v in row:
            if v == "#":
                num_occupied += 1
    return num_occupied


def solution2(grid):
    changed = False
    while True:
        newgrid = copy.deepcopy(grid)
        changed = False
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == "L" and get_adjacent2(grid, x, y) == 0:
                    newgrid[y][x] = "#"
                    changed = True
                elif grid[y][x] == "#" and get_adjacent2(grid, x, y) >= 5:
                    newgrid[y][x] = "L"
                    changed = True
        grid = newgrid
        if not changed:
            break

    num_occupied = 0
    for row in grid:
        for v in row:
            if v == "#":
                num_occupied += 1
    return num_occupied


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    grid = list(map(list, lines))
    ans = solution2(grid)
    print(f"answer: {ans}")
