import os
import sys
import math
import copy
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def solution(lines):
    nums = [int(x) for x in lines[0]]
    nums_len = len(nums)

    cur_idx = 0

    for turn in range(100):
        next_cur = nums[cur_idx + 4] if cur_idx + 4 < nums_len else nums[(cur_idx + 4) % nums_len]

        next3 = []
        for i in range(cur_idx + 1, cur_idx + 4):
            pos = i if i < nums_len else i % nums_len
            next3.append(nums[pos])
        dst = nums[cur_idx] - 1
        while True:
            if dst in next3:
                dst -= 1
                continue
            if dst < 1:
                dst = max(nums)
                continue
            break
        for x in next3:
            nums.remove(x)
        
        dst_idx = nums.index(dst)
        for x in reversed(next3):
            nums.insert(dst_idx + 1, x)
        
        cur_idx = nums.index(next_cur)

        print(f"[{turn}]: {nums}")

    idx1 = nums.index(1)
    ans = ""
    for x in nums[idx1 + 1:]:
        ans += str(x)
    for x in nums[0: idx1]:
        ans += str(x)

    return int(ans)


def solution2(lines):
    nums = [int(x) for x in lines[0]]
    nums += [x for x in range(max(nums) + 1, 1000001)]
    nums_len = len(nums)
    print(nums_len)

    cur_idx = 0

    for turn in range(10000000):
        next_cur = nums[cur_idx + 4] if cur_idx + 4 < nums_len else nums[(cur_idx + 4) % nums_len]

        next3 = []
        for i in range(cur_idx + 1, cur_idx + 4):
            pos = i if i < nums_len else i % nums_len
            next3.append(nums[pos])
        dst = nums[cur_idx] - 1
        while True:
            if dst in next3:
                dst -= 1
                continue
            if dst < 1:
                dst = max(nums)
                continue
            break
        #for x in next3:
        #    del nums[x]
        
        #dst_idx = nums.index(dst)
        dst_idx = 0
        for x in reversed(next3):
            nums.insert(dst_idx + 1, x)
        
        #cur_idx = nums.index(next_cur)
        cur_idx = 0

        #print(f"[{turn}]: {nums}")
        if turn % 100000 == 0:
            print(f"[{turn}]")


    return 0


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
