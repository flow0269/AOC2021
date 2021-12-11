# input_ = open("day10_test").read().splitlines()
input_ = open("day10_input").read().splitlines()

pair_list = [("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")]

chunk_dict = dict(
    zip([x for x, y in pair_list] + [y for x, y in pair_list], [1] * 4 + [-1] * 4)
)

value_dict = dict(zip([y for x, y in pair_list] + [""], [3, 57, 1197, 25137, 0]))
completion_value_dict = dict(zip([x for x, y in pair_list] + [""], [1, 2, 3, 4, 0]))

# part1
def find_bad_char(line_):
    keep_iterating = True
    while (keep_iterating == True) & (len(line_) > 1):
        keep_iterating = False
        z = [chunk_dict[x] for x in line_]
        for id, tuple_ in enumerate(list(zip(z, z[1:]))):
            if tuple_ == (1, -1):
                if (line_[id], line_[id + 1]) in pair_list:
                    keep_iterating = True
                    line_.pop(id + 1)
                    line_.pop(id)
                    break
                else:
                    return (line_[id + 1], [""])

    return ("", line_)


bad_chars = [find_bad_char([x for x in y])[0] for y in input_]

print(sum([value_dict[x] for x in bad_chars]))

# part2


def compute_score(chars):
    sum_ = 0
    for char_ in reversed(chars):
        sum_ *= 5
        sum_ += completion_value_dict[char_]

    return sum_


completion_chars = [find_bad_char([x for x in y])[1] for y in input_]
completion_char_values = [compute_score(x) for x in completion_chars if x != [""]]

completion_char_values.sort()
print(completion_char_values[len(completion_char_values) // 2])

