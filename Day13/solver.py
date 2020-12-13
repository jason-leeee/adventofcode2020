import os
import sys
import math
import copy
import pulp
import random
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def solution(lines):
    timestamp = int(lines[0])
    busids = list(map(int, filter(lambda x: x != "x", lines[1].split(","))))
    print(busids)

    minid = 99999999
    ans = 0
    for busid in busids:
        m = timestamp % busid
        if m > 0:
            m = busid - m
        if m < minid:
            minid = m
            ans = minid * busid
    
    return ans


bus_dict = {}

def get_num(buses, base, step):
    global bus_dict

    ids = buses
    offsets = [bus_dict[bus] for bus in buses]
    entries = list(zip(ids, offsets))
    print(f"entries:{entries}")

    new_base = base
    for x in range(base, 100000000000000000, step):
        bvalid = True
        for busid, offset in entries:
            if (x + offset) % busid != 0:
                bvalid = False
                break
        if bvalid:
            new_base = x
            break
    
    new_step = step
    for x in range(new_base + step, 100000000000000000, step):
        bvalid = True
        for busid, offset in entries:
            if (x + offset) % busid != 0:
                bvalid = False
                break
        if bvalid:
            new_step = x - new_base
            break

    return new_base, new_step


def solution2(lines):
    global bus_dict

    bus_list = [int(busid) for busid in lines[1].split(",") if busid != "x"]
    bus_dict = {int(busid): i for i, busid in enumerate(lines[1].split(",")) if busid != "x"}
    print(bus_list)
    print(bus_dict)

    base = 1
    step = 1
    for i in range(2, len(bus_list) + 1):
        #buses = random.sample(bus_list, i)
        buses = bus_list[:i]
        
        new_base, new_step = get_num(buses, base, step)
        print(f"iteration {i}")
        print(f"\tbuses: {buses}")
        print(f"\tnew_base={new_base}\n\tnew_step={new_step}")

        base = new_base
        step = new_step

    return base


def solution2_pulp(lines):
    busids = {int(busid): i for i, busid in enumerate(lines[1].split(",")) if busid != "x"}
    print(busids)

    prob = pulp.LpProblem('q2', sense=pulp.LpMinimize)
    x = pulp.LpVariable('x', lowBound=0, upBound=None, cat=pulp.LpInteger)
    prob += x
    for k, v in busids.items():
        j = pulp.LpVariable(f'j{k}', lowBound=1, upBound=None, cat=pulp.LpInteger)
        prob += ((x + v) == (k * j))
    prob.solve()

    print(pulp.value(prob.objective))
    print(pulp.value(x))

    return pulp.value(x)


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
