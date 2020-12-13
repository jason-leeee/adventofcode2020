import os
import sys
import math
import copy
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def solution(lines):
    dir_offset = {"N": (0, 1), "S": (0, -1), "W": (-1, 0), "E": (1, 0)}
    dir_rotate = {"N": "W", "W": "S", "S": "E", "E": "N"}
    dir_last = "E"
    x = 0
    y = 0
    for line in lines:
        ins = line[0]
        num = int(line[1:])
        if ins == "L":
            rot = num // 90
            for _ in range(rot):
                dir_last = dir_rotate[dir_last]
        elif ins == "R":
            rot = (360 - num) // 90
            for _ in range(rot):
                dir_last = dir_rotate[dir_last]
        elif ins == "F":
            x_offset, y_offset = dir_offset[dir_last]
            x += x_offset * num
            y += y_offset * num
        else:
            x_offset, y_offset = dir_offset[ins]
            x += x_offset * num
            y += y_offset * num
    return abs(x) + abs(y)


def anti_rotate_90(x, y):
    oldx = x
    x = -y
    y = oldx
    return x, y


def solution2(grid):
    dir_offset = {"N": (0, 1), "S": (0, -1), "W": (-1, 0), "E": (1, 0)}
    sx = 0
    sy = 0
    wx = 10
    wy = 1
    for line in lines:
        ins = line[0]
        num = int(line[1:])
        if ins == "L":
            rot = num // 90
            for _ in range(rot):
                wx, wy = anti_rotate_90(wx, wy)
        elif ins == "R":
            rot = (360 - num) // 90
            for _ in range(rot):
                wx, wy = anti_rotate_90(wx, wy)
        elif ins == "F":
            sx += wx * num
            sy += wy * num
        else:
            x_offset, y_offset = dir_offset[ins]
            wx += x_offset * num
            wy += y_offset * num
        print(f"[{ins}{num}] ship({sx},{sy}) wp({wx},{wy})")
    return abs(sx) + abs(sy)


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
