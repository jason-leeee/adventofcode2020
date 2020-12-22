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


def resolve_input(lines):
    lseps = split_list(lines)
    player1 = list(map(int, lseps[0][1:]))
    player2 = list(map(int, lseps[1][1:]))
    return player1, player2


def solution(lines):
    player1, player2 = resolve_input(lines)

    print(player1)
    print(player2)

    while len(player1) > 0 and len(player2) > 0:
        m1 = player1[0]
        m2 = player2[0]
        
        mappend = sorted([m1, m2], reverse=True)
        if m1 > m2:
            player1 = player1[1:] + mappend
            player2 = player2[1:]
        else:
            player1 = player1[1:]
            player2 = player2[1:] + mappend

    player_win = player1 if len(player1) > 0 else player2
    score = 0
    for i, x in enumerate(reversed(player_win)):
        score += (i + 1) * x
    return score


def encode_players(player1, player2):
    c1 = "|".join(map(str, player1))
    c2 = "|".join(map(str, player2))
    return c1 + "+" + c2


def subgame(player1, player2):
    history = {}
    
    while len(player1) > 0 and len(player2) > 0:
        encoded_players = encode_players(player1, player2)
        if encoded_players in history:
            winner = 1
            deck = player1
            break
        else:
            history[encoded_players] = True

            m1 = player1[0]
            m2 = player2[0]
            player1 = player1[1:]
            player2 = player2[1:]

            if len(player1) >= m1 and len(player2) >= m2:
                subwinner, _ = subgame(copy.deepcopy(player1[:m1]), copy.deepcopy(player2[:m2]))
            else:
                subwinner = 1 if m1 > m2 else 2

            if subwinner == 1:
                player1 += [m1, m2]
            else:
                player2 += [m2, m1]

    winner, deck = (1, player1) if len(player1) > 0 else (2, player2)
    return winner, deck


def solution2(lines):
    player1, player2 = resolve_input(lines)

    print(player1)
    print(player2)

    _, deck = subgame(player1, player2)
    score = 0
    for i, x in enumerate(reversed(deck)):
        score += (i + 1) * x
    return score


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
