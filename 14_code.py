from collections import Counter
from copy import copy
from itertools import permutations

input_ = open("day14_input").read().splitlines()
# input_ = open("day14_test").read().splitlines()

template = input_[0]

rules = [x.split(" -> ") for x in input_[2:]]

rule_dict = {x: x[0] + y + x[1] for x, y in rules}
all_letters = [x[z] for z in range(2) for x, _ in rules]

l = set(permutations(all_letters, 2))

pair_counts = {"".join(x): 0 for x in l}
for x in zip(template, template[1:]):
    pair_counts["".join(x)] += 1

rule_map = {"".join(x): (x[0] + y, y + x[1]) for x, y in rules}
rule_map_single = {"".join(x): y for x, y in rules}


def iter_rules(pair_counts, l_counts):
    global rule_map, rule_map_single

    pc_copy = copy(pair_counts)
    for pair_, count_ in pair_counts.items():
        pc_copy[pair_] -= count_
        pc_copy[rule_map[pair_][0]] += count_
        pc_copy[rule_map[pair_][1]] += count_
        l_counts[rule_map_single[pair_][0]] += count_

    return pc_copy, l_counts


l_counts = Counter(template)
for x in range(40):
    pair_counts, l_counts = iter_rules(pair_counts, l_counts)
    if x == 9:
        letter_counts = Counter(l_counts)
        mc = letter_counts.most_common()
        print("part1", mc[0][1] - mc[-1][1])

letter_counts = Counter(l_counts)
mc = letter_counts.most_common()
print("part2", mc[0][1] - mc[-1][1])
