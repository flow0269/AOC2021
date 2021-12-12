from copy import copy

# part 1 methodology:
# 1: get a dictionary of all cave routes from every cave (in get_input method)
# 2: construct a recursive loop that tests every possible route from every cave, ensuring that the conditions are met
# 3: if an endpoint is met with all of the conditions met, increase global counter by 1


def get_input():
    input_ = open("day12_input").read().splitlines()
    paths = [x.split("-") for x in input_]
    caves = list(set([y for x in input_ for y in x.split("-")]))
    path_dict = dict()
    for cave_ in caves:
        path_dict[cave_] = []
        for path_ in paths:
            if cave_ in path_:
                path_dict[cave_].append([x for x in path_ if x != cave_][0])
    return caves, path_dict


def find_pathway_part1(cave_count_dict, path_, cave1="start"):
    global path_dict, path_count, found_path_set
    for cave2 in path_dict[cave1]:
        if (cave_count_dict[cave2] > 0) & cave2[0].islower():
            continue
        elif cave2 == "end":
            if "".join(path_) not in found_path_set:
                found_path_set.add("".join(path_))
                path_count += 1
        else:
            cave_count_dict2 = copy(cave_count_dict)
            cave_count_dict2[cave2] += 1
            path2 = copy(path_)
            path2.append(cave2)
            find_pathway_part1(cave_count_dict2, path2, cave2)

    return


def find_pathway_part2(cave_count_dict, path_, twice_, cave1="start"):
    global path_dict, path_count, found_path_set

    for cave2 in path_dict[cave1]:
        if cave2 == "start":
            continue
        elif cave2 == "end":
            if "".join(path_) not in found_path_set:
                found_path_set.add("".join(path_))
                path_count += 1
        elif (cave_count_dict[cave2] > 0) & cave2[0].islower() & twice_:
            continue
        elif (cave_count_dict[cave2] > 1) & cave2[0].islower():
            continue
        else:
            cave_count_dict2 = copy(cave_count_dict)
            cave_count_dict2[cave2] += 1
            path2 = copy(path_)
            path2.append(cave2)
            if ((cave_count_dict2[cave2] > 1) & cave2[0].islower()) | twice_:
                find_pathway_part2(cave_count_dict2, path2, True, cave2)
            else:
                find_pathway_part2(cave_count_dict2, path2, False, cave2)

    return


def initialize():
    # initialize global variables
    global caves, path_count, found_path_set
    cave_count_dict = dict()
    for x in caves:
        cave_count_dict[x] = 0
    cave_count_dict["start"] = 1
    path_count = 0
    found_path_set = set()
    return cave_count_dict


caves, path_dict = get_input()

initial_count_dict = initialize()
find_pathway_part1(initial_count_dict, [])
print("part1", path_count)

initial_count_dict = initialize()
find_pathway_part2(initial_count_dict, [], False)
print("part2", path_count)
