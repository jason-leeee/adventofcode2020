import os
import sys
import math
import random
import itertools
import numpy as np


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


def build_fieldmap(str_fields):
    fieldmap = {}
    for row in str_fields:
        seps = row.split(": ")
        seps = seps[1].split(" or ")
        for i in range(2):
            [m, n] = seps[i].split("-")
            for x in range(int(m), int(n) + 1):
                fieldmap[x] = True
    return fieldmap


def build_fieldmap2(str_fields):
    fieldmap = {}
    occurmap = {}
    for row in str_fields:
        seps = row.split(": ")
        field = seps[0]
        fieldmap[field] = {}
        seps = seps[1].split(" or ")
        for i in range(2):
            [m, n] = seps[i].split("-")
            for x in range(int(m), int(n) + 1):
                fieldmap[field][x] = True
                occurmap[x] = True
    return fieldmap, occurmap


def solution(lines):
    lseps = split_list(lines)

    str_fields = lseps[0]
    str_nearby_tickets = lseps[2]

    fieldmap, occurmap = build_fieldmap(str_fields)

    invalid_tickets = []
    for row in str_nearby_tickets[1:]:
        tickets = list(map(int, row.split(",")))
        tickets = list(filter(lambda t: t not in occurmap, tickets))
        invalid_tickets.extend(tickets)

    return sum(invalid_tickets)


def solution2(lines):
    lseps = split_list(lines)

    str_fields = lseps[0]
    str_my_ticket = lseps[1]
    str_nearby_tickets = lseps[2]

    # get field hashmap
    fieldmap, occurmap = build_fieldmap2(str_fields)

    # get all tickets
    all_fields = list(fieldmap.keys())
    all_tickets = []
    for row in str_my_ticket[1:] + str_nearby_tickets[1:]:
        tickets = list(map(int, row.split(",")))

        bvalid = True
        for t in tickets:
            if t not in occurmap:
                bvalid = False
                break
        
        if bvalid:
            all_tickets.append(tickets)
    print(all_fields)
    print(all_tickets)

    # convert tickets to array
    num_tickets = len(all_tickets)
    num_fields = len(all_tickets[0])
    arr_tickets = np.zeros((num_tickets, num_fields), dtype=np.int32)
    for i, ticket in enumerate(all_tickets):
        for j, v in enumerate(ticket):
            arr_tickets[i, j] = v
    print(arr_tickets)

    # get possible fileds for each column
    col_fields = {col: [] for col in range(num_fields)}
    for col in range(num_fields):
        for field in all_fields:
            bvalid = True
            for x in arr_tickets[:, col]:
                if x not in fieldmap[field]:
                    bvalid = False
            if bvalid:
                col_fields[col].append(field)
    print(col_fields)

    # search for the fixed order of fields
    # by iteratively fixing the fields that have only one option
    while True:
        col_onefield = []
        for col, fields in col_fields.items():
            if len(fields) == 1:
                col_onefield.append(fields[0])
        if len(col_onefield) == num_fields:
            break
        else:
            for col in col_fields.keys():
                if len(col_fields[col]) > 1:
                    for field_del in col_onefield:
                        if field_del in col_fields[col]:
                            col_fields[col].remove(field_del)
    print(col_fields)

    # compute the answer on my ticket
    my_ticket = list(map(int, str_my_ticket[1].split(",")))
    print(my_ticket)
    ans = 1
    for col, field in col_fields.items():
        if field[0][:9] == "departure":
            ans *= my_ticket[col]
    return ans


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
