import os
import sys
import math
import copy
import itertools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def split_list(lines):
    lseps = []
    lsep = []
    for line in lines:
        if line:
            lsep.append(line)
        else:
            lseps.append(lsep)
            lsep = []
    lseps.append(lsep)
    return lseps


def is_all_rules_decoded(subrules, decoded):
    all_decoded = True
    for subrule in subrules:
        for subid in subrule:
            if subid not in decoded:
                all_decoded = False
                break
        if not all_decoded:
            break
    return all_decoded


def generate_rule_values(base, rule, rvalues, rret):
    if not rule:
        rret.append(base)
        return
    rid = rule[0]
    rest = rule[1:]
    values = rvalues[rid]
    for v in values:
        generate_rule_values(base + v, rest, rvalues, rret)


def decode_init(rawrules):
    rulesmap = {}
    rvalues = {}
    decoded = {}
    for rule in rawrules:
        [rid, rtext] = rule.split(": ")
        rid = int(rid)
        if '"' in rule:
            c = rule.split('"')[1]
            rvalues[rid] = [c]
            decoded[rid] = True
        else:
            rulesmap[rid] = []
            subrules = rtext.split(" | ")
            for subrule in subrules:
                rulesmap[rid].append(list(map(int, subrule.split(" "))))
    return rulesmap, rvalues, decoded

def decode_rules(rulesmap, rvalues, decoded):
    while 0 in rulesmap:
        for rid in list(rulesmap.keys()):
            subrules = rulesmap[rid]
            all_decoded = is_all_rules_decoded(subrules, decoded)
            if all_decoded:
                #print(f"all_decoded rid: {rid}")
                rvalues[rid] = []
                for subrule in subrules:
                    newrvalues = []
                    generate_rule_values("", subrule, rvalues, newrvalues)
                    rvalues[rid].extend(newrvalues)
                decoded[rid] = True
                del rulesmap[rid]
                #print(f"\trvalues[rid]: {rvalues[rid]}")
    return rvalues


def solution(lines):
    [rawrules, msgs] = split_list(lines)

    rulesmap, rvalues, decoded = decode_init(rawrules)
    #print(f"init rulesmap: {rulesmap}")
    #print(f"init rvalues : {rvalues}")
    #print(f"init decoded : {decoded}")

    rvalues = decode_rules(rulesmap, rvalues, decoded)

    rule0map = {rtext: True for rtext in rvalues[0]}
    #print(f"rule 0: {rule0}")

    num_valid = sum([1 if msg in rule0map else 0 for msg in msgs])
    return num_valid


def solution2(lines):
    [rawrules, msgs] = split_list(lines)

    rulesmap, rvalues, decoded = decode_init(rawrules)
    rvalues = decode_rules(rulesmap, rvalues, decoded)
    #print(f"rule 42: {rvalues[42]}")
    #print(f"rule 31: {rvalues[31]}")

    num_valid = 0
    for msg in msgs:
        rawmsg = copy.deepcopy(msg)

        r42 = rvalues[42]
        r31 = rvalues[31]
        len_r42 = len(r42[0])
        len_r31 = len(r31[0])

        n_42 = 0
        while True:
            if msg[:len_r42] not in r42:
                break
            msg = msg[len_r42:]
            n_42 += 1
        
        n_31 = 0
        while True:
            if msg[:len_r31] not in r31:
                break
            msg = msg[len_r31:]
            n_31 += 1

        if n_31 >= 1 and n_42 > n_31 and len(msg) == 0:
            num_valid += 1

    return num_valid


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
