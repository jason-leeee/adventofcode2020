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


def is_loop_rule(rid, subrules):
    is_loop = False
    for subrule in subrules:
        for subid in subrule:
            if subid == rid:
                is_loop = True
                break
        if is_loop:
            break
    return is_loop


def potential_msgs(rid, msgs, rvalues):
    newmsgs = []
    for msg in msgs:
        is_any_rule = False
        for rule in rvalues[rid]:
            if rule in msg:
                is_any_rule = True
                break
        if msg not in rvalues[0] and is_any_rule:
            newmsgs.append(msg)
    return newmsgs


def reduce8(msg, rules, retmsgs):
    rule_hit = False
    rlen = len(rules[0])
    for i in range(len(msg) - rlen):
        if msg[i: i + rlen] in rules:
            reduce8(msg[:i] + msg[i + rlen:], rules, retmsgs)
            rule_hit = True
    if not rule_hit:
        retmsgs.append(msg)


def solution4(lines):
    [rawrules, msgs] = split_list(lines)

    rulesmap, rvalues, decoded = decode_init(rawrules)
    for rid in list(rulesmap.keys()):
        subrules = rulesmap[rid]
        is_loop = is_loop_rule(rid, subrules)
        if is_loop:
            newsubrules = [subrules[0]]
            print(f"loop rule {rid}: {subrules} => {newsubrules}")
            rulesmap[rid] = newsubrules

    rvalues = decode_rules(rulesmap, rvalues, decoded)

    print(f"rule 42: {rvalues[42]}")
    print(f"rule 31: {rvalues[31]}")

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


def solution2(lines):
    [rawrules, msgs] = split_list(lines)

    rulesmap, rvalues, decoded = decode_init(rawrules)
    for rid in list(rulesmap.keys()):
        subrules = rulesmap[rid]
        is_loop = is_loop_rule(rid, subrules)
        if is_loop:
            newsubrules = [subrules[0]]
            print(f"loop rule {rid}: {subrules} => {newsubrules}")
            rulesmap[rid] = newsubrules

    rvalues = decode_rules(rulesmap, rvalues, decoded)
    rule0map = {rtext: True for rtext in rvalues[0]}
    num_valid = sum([1 if msg in rule0map else 0 for msg in msgs])

    #print(f"rule 42: {rvalues[42]}")
    #print(f"rule 31: {rvalues[31]}")
    #print(f"rule 11: {rvalues[11]}")
    
    msgs8 = potential_msgs(8, msgs, rvalues)
    msgs11 = potential_msgs(11, msgs, rvalues)
    print("potential msg 8:")
    for msg in msgs8:
        print(f"\t{msg}")
    print("potential msg 11:")
    for msg in msgs11:
        print(f"\t{msg}")

    return 0

    #print(f"rule 8: {rvalues[8]}")
    rule8msgs = copy.deepcopy(msgs)
    for msgid in range(len(msgs)):
        msg = msgs[msgid]
        for rule in rvalues[8]:
            rlen = len(rule)
            for i in range(len(msg) - rlen):
                if msg[i: i + rlen] == rule:
                    match_min = i
                    match_max = i + rlen
                    """
                    j = i
                    while j - rlen >= 0:
                        j -= rlen
                        if msg[j: j + rlen] in rvalues[8]:
                            match_min = j
                        else:
                            break
                    """
                    j = i
                    while j + rlen <= len(msg):
                        j += rlen
                        if msg[j: j + rlen] in rvalues[42]:
                            match_max = j + rlen
                        else:
                            break
                    newmsg = msg[0:match_min] + rule + msg[match_max:]
            print(f"rule 8 msg: {msg} ->")
            print(f"            {newmsg}")
            rule8msgs[msgid] = newmsg
                    
            #if rule in msg:
            #    print(f"\t{msg}")

    """
    #print(f"rule 11: {rvalues[11]}")
    rule11msgs = copy.deepcopy(msgs)
    for msgid in range(len(msgs)):
        msg = msgs[msgid]
        for rule in rvalues[8]:
            rlen = len(rule)
            for i in range(len(msg) - rlen):
                if msg[i: i + rlen] == rule:
                    halflen = rlen // 2
                    match_min = i
                    match_max = i + rlen

                    j = i
                    while j - halflen >= 0:
                        j -= halflen
                        if msg[j: j + halflen] in rvalues[42]:
                            match_min = j
                        else:
                            break
                    j = i + halflen
                    while j + halflen <= len(msg):
                        j += halflen
                        if msg[j: j + halflen] in rvalues[31]:
                            match_max = j + halflen
                        else:
                            break
                    newmsg = msg[0:match_min] + rule + msg[match_max:]
        print(f"rule 11 msg: {msg} -> ")
        print(f"             {newmsg}")
        rule11msgs[msgid] = newmsg
    """
    
    return num_valid


def solution3(lines):
    [rawrules, msgs] = split_list(lines)

    # init leaf rvalues
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
    print(f"init rulesmap: {rulesmap}")
    print(f"init rvalues : {rvalues}")
    print(f"init decoded : {decoded}")

    MAX_LOOP = 3
    for rid in list(rulesmap.keys()):
        subrules = rulesmap[rid]
        is_loop = is_loop_rule(rid, subrules)
        if is_loop:
            print(f"loop rule: {rid}")
            if rid == 8:
                newsubrules = [subrules[0]]
                base_rule = subrules[0]
                new_rule = subrules[0]
                for _ in range(MAX_LOOP):
                    new_rule = new_rule + base_rule
                    newsubrules.append(new_rule)
                print(f"newsubrules: {newsubrules}")
            elif rid == 11:
                newsubrules = [subrules[0]]
                lrule = [subrules[0][0]]
                rrule = [subrules[0][1]]
                new_rule = subrules[0]
                for _ in range(MAX_LOOP):
                    new_rule = lrule + new_rule + rrule
                    newsubrules.append(new_rule)
                print(f"newsubrules: {newsubrules}")
            rulesmap[rid] = newsubrules

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

    rule0map = {rtext: True for rtext in rvalues[0]}
    #print(f"rule 0: {rule0}")

    num_valid = sum([1 if msg in rule0map else 0 for msg in msgs])
    return num_valid


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution4(lines)
    print(f"answer: {ans}")
