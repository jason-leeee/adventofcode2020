import os
import sys
import math
import copy
import random
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def apply_bitmask(val, bitmask):
    bitval = bin(val)[2:]

    for _ in range(len(bitmask) - len(bitval)):
        bitval = "0" + bitval

    print(f"bitval : {bitval}")
    print(f"bitmask: {bitmask}")

    retval = ""
    for i in range(len(bitmask)):
        if bitmask[i] != "X":
            retval += bitmask[i]
        else:
            retval += bitval[i]

    print(f"retval : {retval}")

    return int(retval, 2)


def solution(lines):
    mem = {}
    bitmask = ""

    for line in lines:
        if line[:3] == "mem":
            op, val = line.split(" = ")
            addr = int(op[4:-1])
            val = int(val)
            mem[addr] = apply_bitmask(val, bitmask)
        else:
            bitmask = line[7:]
    print(mem)
    
    return sum(mem.values())


def fill_x(addr, pos):
    if pos == len(addr):
        return [addr]
    if addr[pos] == "X":
        retlist = []
        addrnew = addr[:pos] + "0" + addr[pos + 1:]
        retlist.extend(fill_x(addrnew, pos + 1))
        addrnew = addr[:pos] + "1" + addr[pos + 1:]
        retlist.extend(fill_x(addrnew, pos + 1))
        return retlist
    return fill_x(addr, pos + 1)


def decode_addr(addr, bitmask):
    bitaddr = bin(addr)[2:]

    for _ in range(len(bitmask) - len(bitaddr)):
        bitaddr = "0" + bitaddr

    print(f"bitaddr: {bitaddr}")
    print(f"bitmask: {bitmask}")

    retaddr = ""
    for i in range(len(bitmask)):
        if bitmask[i] == "0":
            retaddr += bitaddr[i]
        else:
            retaddr += bitmask[i]

    print(f"retaddr: {retaddr}")

    bitaddrs = fill_x(retaddr, 0)
    addrs = [int(bitaddr, 2) for bitaddr in bitaddrs]

    return addrs


def solution2(lines):
    mem = {}
    bitmask = ""

    for line in lines:
        if line[:3] == "mem":
            op, val = line.split(" = ")
            addr = int(op[4:-1])
            val = int(val)
            addrs = decode_addr(addr, bitmask)
            for addr in addrs:
                mem[addr] = val
        else:
            bitmask = line[7:]
    
    return sum(mem.values())


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
