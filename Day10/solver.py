import os
import sys
import math
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def solution(nums):
    nums = [0] + sorted(nums) + [max(nums) + 3]
    diff = {1: 0, 3: 0}
    for i in range(len(nums) - 1):
        diff[nums[i + 1] - nums[i]] += 1
    return diff[1] * diff[3]


def solution2(nums):
    nums = [0] + sorted(nums) + [max(nums) + 3]
    dp = {0: 1}
    for k in nums[1:]:
        dp[k] = dp.get(k - 1, 0) + dp.get(k - 2, 0) + dp.get(k - 3, 0)
    return dp[max(nums)]


def solution2_Om(nums):
    target = max(nums) + 3
    nums = [0] + nums + [target]
    nmap = {k: True for k in nums}
    dp = {0: 1}
    for k in range(1, target + 1):
        if k in nmap:
            dp[k] = dp.get(k - 1, 0) + dp.get(k - 2, 0) + dp.get(k - 3, 0)
    return dp[target]


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    nums = list(map(int, lines))
    ans = solution2(nums)
    print(f"answer: {ans}")
