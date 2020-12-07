import os
import sys
import math
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


gbags1 = {}
visited1 = {}

gbags2 = {}


def dfs1(node):
    if node not in visited1:
        visited1[node] = True
        for neighbor in gbags1.get(node, []):
            dfs1(neighbor)


def solution(lines):
    for line in lines:
        line = line.rstrip(".")
        [parent, children] = line.split(" contain ")
        parent = parent.rstrip("s")
        if children != "no other bags":
            seps = children.split(", ")
            for child in seps:
                quantity = int(child[0])
                child = child.rstrip("s")
                child = child[2:]
                print(f"{parent} -> ({quantity}) {child}")
                gbags1[child] = gbags1.get(child, []) + [parent]

    dfs1("shiny gold bag")
    return len(visited1) - 1


def dfs2(node):
    bag, quantity = node
    if gbags2[bag]:
        m = 0
        for cbag, cquantity in gbags2[bag]:
            m += cquantity + dfs2((cbag, cquantity)) * cquantity
        return m
    return 0


def solution2(lines):
    for line in lines:
        line = line.rstrip(".")
        [parent, children] = line.split(" contain ")
        parent = parent.rstrip("s")
        if children != "no other bags":
            seps = children.split(", ")
            for child in seps:
                quantity = int(child[0])
                child = child.rstrip("s")
                child = child[2:]
                print(f"{parent} -> ({quantity}) {child}")
                gbags2[parent] = gbags2.get(parent, []) + [(child, quantity)]
        else:
            gbags2[parent] = []
    return dfs2(("shiny gold bag", 1))


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
