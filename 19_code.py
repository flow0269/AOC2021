from copy import copy
from collections import deque
import random


def equiv_beacons(bcn1, bcn2):
    return set(bcn1) == set(bcn2)


def get_position_shift(x1, x2):
    x1 = [abs(x) for x in x1]
    x2 = [abs(x) for x in x2]
    positions = []
    for x in x1:
        positions.append(x2.index(x))
    return positions


def scanner_loc(s1, s2):
    origin2 = s2[0]
    rels2 = [[abs(bcn[0] - origin2[0]), abs(bcn[1] - origin2[1]), abs(bcn[2] - origin2[2])] for bcn in s2]
    for origin1 in s1:
        rels1 = [[abs(bcn[0] - origin1[0]), abs(bcn[1] - origin1[1]), abs(bcn[2] - origin1[2])] for bcn in s1]
        if sum([sum([equiv_beacons(x1, x2) for x1 in rels2]) for x2 in rels1]) >= 12:
            for id_, x1 in enumerate(rels1):
                if equiv_beacons(x1, rels2[1]):
                    # print(x1, rels2[1])
                    x1 = [s1[id_][0] - origin1[0], s1[id_][1] - origin1[1], s1[id_][2] - origin1[2]]
                    x2 = [s2[1][0] - origin2[0], s2[1][1] - origin2[1], s2[1][2] - origin2[2]]

                    positions_ = get_position_shift(copy(x1), copy(x2))
                    x3 = [x2[positions_[0]], x2[positions_[1]], x2[positions_[2]]]
                    signs_ = [x // y for x, y in zip(x1, x3)]
                    origin2 = [origin2[positions_[0]], origin2[positions_[1]], origin2[positions_[2]]]
                    offsets = [x - (y * z) for (x, y, z) in zip(origin1, origin2, signs_)]
                    return offsets, signs_, positions_


def overlapping_scanners(beacons1, beacons2):
    for zero_beacon2 in beacons2[:-11]:
        rels2 = set(
            [
                frozenset(
                    [abs(bcn[0] - zero_beacon2[0]), abs(bcn[1] - zero_beacon2[1]), abs(bcn[2] - zero_beacon2[2])]
                )
                for bcn in beacons2
            ]
        )
        for bcn_num2, zero_beacon1 in enumerate(beacons1):
            rels1 = set(
                [
                    frozenset(
                        [abs(bcn[0] - zero_beacon1[0]), abs(bcn[1] - zero_beacon1[1]), abs(bcn[2] - zero_beacon1[2])]
                    )
                    for bcn in beacons1
                ]
            )
            intersect_ = rels2.intersection(rels1)
            equiv_count = len(intersect_)
            if equiv_count >= 12:
                print("found overlap at beacon numbers", bcn_num2)
                rels1 = [
                    [abs(bcn[0] - zero_beacon1[0]), abs(bcn[1] - zero_beacon1[1]), abs(bcn[2] - zero_beacon1[2])]
                    for bcn in beacons1
                ]
                rels2 = [
                    [abs(bcn[0] - zero_beacon2[0]), abs(bcn[1] - zero_beacon2[1]), abs(bcn[2] - zero_beacon2[2])]
                    for bcn in beacons2
                ]
                equiv_map = [sum([equiv_beacons(x1, x2) for x1 in rels2]) for x2 in rels1]
                scan1_beacons = [x for x, y in zip(beacons1, equiv_map) if y == 1]
                equiv_map = [sum([equiv_beacons(x1, x2) for x1 in rels1]) for x2 in rels2]
                scan2_beacons = [x for x, y in zip(beacons2, equiv_map) if y == 1]
                return scan1_beacons, scan2_beacons

    return [], []


def reorient_scanner(offset_, sign_, positions_, beacons, scanner_bag, oriented_beacons, scanner_id):
    oriented_beacons[scanner_id] = []
    for beacon_ in beacons:
        x1 = tuple(beacon_[z] for z in positions_)
        x2 = tuple(x1[z] * sign_[z] for z in range(3))
        x3 = tuple(x2[z] + offset_[z] for z in range(3))
        oriented_beacons[scanner_id].append(x3)
        scanner_bag.add(x3)

    return scanner_bag, oriented_beacons


def scanner_distance(scanner1, scanner2):
    return abs(scanner1[0] - scanner2[0]) + abs(scanner1[1] - scanner2[1]) + abs(scanner1[2] - scanner2[2])


n_scanners = 35

input_ = open("day19_input").read().split("--- ")[1:]
input2 = [x[(x.index(" ---") + 5) :] for x in input_]
input3 = [[tuple(int(y) for y in x.split(",")) for x in input2[z].split("\n") if x != ""] for z in range(n_scanners)]

scanner_list = list(range(n_scanners))

oriented_beacons = {}
overlaps = {}
offsets = {}
signs = {}
positions = {}
beacon_bag = set()
scanner_queue = deque()

scanner_queue.append(0)
scanner_list.remove(0)
oriented_beacons[0] = input3[0]
while (len(scanner_list) > 0) and (len(scanner_queue) > 0):
    found = False
    ref_scanner = scanner_queue[-1]
    found_beacons = oriented_beacons[ref_scanner]
    random.shuffle(scanner_list)
    print(len(scanner_list), "scanners left to reorient")
    for scanner_ in scanner_list:
        new_beacons = input3[scanner_]

        scan1_beacons, scan2_beacons = overlapping_scanners(found_beacons, new_beacons)
        if len(scan1_beacons) > 0:
            scanner_queue.append(scanner_)
            scanner_list.remove(scanner_)
            offsets_, signs_, positions_ = scanner_loc(scan1_beacons, scan2_beacons)
            offsets[scanner_] = offsets_
            signs[scanner_] = signs_
            positions[scanner_] = positions_
            beacon_bag, oriented_beacons = reorient_scanner(
                offsets_, signs_, positions_, copy(new_beacons), beacon_bag, oriented_beacons, scanner_
            )
            print("overlap", scanner_, ref_scanner, "beacon count", len(list(beacon_bag)))
            found = True
            break

    if not found:
        scanner_queue.pop()

print("part1", len(beacon_bag))
distances = [scanner_distance(x, y) for x in offsets.values() for y in offsets.values()]
print("part2", max(distances))

