from sys import maxsize
from math import prod

input_ = open("day16_input").read()
ini_string = input_

bin_code = "{0:04b}".format(int(ini_string, 16))
bin_code = "0" * (len(ini_string) * 4 - len(bin_code)) + bin_code

print(len(ini_string), len(bin_code))


def literal_value_func(bin_):
    z = 0
    packets = []
    while bin_[z] == "1":
        packets.extend(bin_[z + 1 : z + 5])
        z += 5
    packets.extend(bin_[z + 1 : z + 5])
    z += 5
    return int("".join(packets), 2), z


def expression_value(packet_id, literal_values):
    if packet_id == 0:
        return sum(literal_values)
    elif packet_id == 1:
        return prod(literal_values)
    elif packet_id == 2:
        return min(literal_values)
    elif packet_id == 3:
        return max(literal_values)
    elif packet_id == 5:
        if literal_values[0] > literal_values[1]:
            return 1
        else:
            return 0
    elif packet_id == 6:
        if literal_values[0] < literal_values[1]:
            return 1
        else:
            return 0
    elif packet_id == 7:
        if literal_values[0] == literal_values[1]:
            return 1
        else:
            return 0


def find_subpackets(bin_, max_len, n_subs, start_index=0):
    literal_values = []
    version_sum = 0
    sub_count = 0
    z = 0
    while (z < max_len - 6) & (sub_count < n_subs):
        packet_version = int(bin_[z : z + 3], 2)
        packet_id = int(bin_[z + 3 : z + 6], 2)
        z += 6
        if packet_id == 4:
            literal_value, sub_len = literal_value_func(bin_[z:])
            z += sub_len
        elif bin_[z] == "0":
            sub_len = int(bin_[z + 1 : z + 16], 2)
            z += 16
            literal_values_sub, z, sub_version_sum = find_subpackets(bin_[z:], sub_len, maxsize, z)
            literal_value = expression_value(packet_id, literal_values_sub)
            version_sum += sub_version_sum
        else:
            sub_len = int(bin_[z + 1 : z + 12], 2)
            z += 12
            literal_values_sub, z, sub_version_sum = find_subpackets(bin_[z:], maxsize, sub_len, z)
            literal_value = expression_value(packet_id, literal_values_sub)
            version_sum += sub_version_sum
        sub_count += 1
        literal_values.append(literal_value)
        version_sum += packet_version
    return literal_values, z + start_index, version_sum


literal_values, total_length, version_sum = find_subpackets(bin_code, len(bin_code), maxsize)


print("part1", version_sum, "part2", literal_values[0])
