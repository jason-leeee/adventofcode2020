import os
import sys
import math
import itertools
import numpy as np


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def resolve_input(lines):
    ingredients = []
    allergens = []
    rules = []
    possible_contains = {}

    for line in lines:
        [ings, alles] = line.split(" (contains ")
        ings = ings.split(" ")
        alles = alles[:-1]
        alles = alles.split(", ")

        for ing in ings:
            for alle in alles:
                possible_contains[ing] = possible_contains.get(ing, []) + [alle]

        ingredients.extend(ings)
        allergens.extend(alles)
        rules.append((ings, alles))

    for k in possible_contains:
        possible_contains[k] = list(set(possible_contains[k]))

    ingredients = list(set(ingredients))
    allergens = list(set(allergens))
    return ingredients, allergens, rules, possible_contains


def get_impossible_ingredients(ingredients, allergens, rules, possible_contains):
    impossible_ings = {}
    for ing in ingredients:
        contain_any = False
        for alle in possible_contains[ing]:
            is_possible = True
            for rule_ings, rule_alles in rules:
                if alle in rule_alles and ing not in rule_ings:
                    is_possible = False
                    break
            if is_possible:
                contain_any = True
                break
        if not contain_any:
            impossible_ings[ing] = True

    return impossible_ings


def solution(nums):
    ingredients, allergens, rules, possible_contains = resolve_input(lines)
    print(f"ingredients: {ingredients}")
    print(f"allergens: {allergens}")
    print(f"rules: {rules}")
    print(f"possible_contains: {possible_contains}")

    impossible_ings = get_impossible_ingredients(ingredients, allergens, rules, possible_contains)
    print(f"impossible_ings: {list(impossible_ings.keys())}")

    total_occur = 0
    for rule_ings, rule_alles in rules:
        for rule_ing in rule_ings:
            total_occur += 1 if rule_ing in impossible_ings else 0

    return total_occur


def remove_impossible_ingredients(ingredients, rules, possible_contains, impossible_ings):
    ingredients = [ing for ing in ingredients if ing not in impossible_ings]
    
    newrules = []
    for rule_ings, rule_alles in rules:
        rule_ings = [ing for ing in rule_ings if ing not in impossible_ings]
        newrules.append((rule_ings, rule_alles))

    for impossible_ing in impossible_ings:
        del possible_contains[impossible_ing]

    return ingredients, newrules, possible_contains


def search_match(depth, assigns, ings, alles, rules, results):
    if depth == len(ings):
        print(f"finishing assigns: {assigns}")
        results.append(np.copy(assigns))
        return

    ing = ings[depth]
    for i, alle in enumerate(alles):
        if i in assigns:
            continue
        all_rule_valid = True
        for rule_ings, rule_alles in rules:
            if alle in rule_alles and ing not in rule_ings:
                all_rule_valid = False
                break
        if all_rule_valid:
            assigns[depth] = i
            search_match(depth + 1, assigns, ings, alles, rules, results)
            assigns[depth] = -1


def solution2(nums):
    ingredients, allergens, rules, possible_contains = resolve_input(lines)
    print(f"ingredients: {ingredients}")
    print(f"allergens: {allergens}")
    print(f"rules: {rules}")
    print(f"possible_contains: {possible_contains}")

    impossible_ings = get_impossible_ingredients(ingredients, allergens, rules, possible_contains)
    print(f"impossible_ings: {list(impossible_ings.keys())}")

    print("\n")

    ingredients, rules, possible_contains = remove_impossible_ingredients(ingredients, rules, possible_contains, impossible_ings)
    print(f"ingredients: {ingredients}")
    print(f"allergens: {allergens}")
    print(f"rules: {rules}")
    print(f"possible_contains: {possible_contains}")

    # only 8 ingredients and 8 allergens are left, so brute-force
    results = []
    search_match(
        depth=0,
        assigns=np.array([-1] * len(ingredients), dtype=np.int8),
        ings=ingredients,
        alles=allergens,
        rules=rules,
        results=results
    )
    assert len(results) == 1
    assigns = results[0]

    matches = []
    for i, j in enumerate(assigns):
        ing = ingredients[i]
        alle = allergens[j]
        matches.append((ing, alle))
    matches = sorted(matches, key=lambda match: match[1])
    
    dangerous_list = ""
    for ing, alle in matches:
        dangerous_list += ing + ","
    dangerous_list = dangerous_list[:-1]

    return dangerous_list


def read_input():
    with open(f"{CURRENT_DIR}/input.txt", "r") as fread:
        lines = fread.read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read_input()
    ans = solution2(lines)
    print(f"answer: {ans}")
