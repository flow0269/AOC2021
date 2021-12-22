from ast import literal_eval
from math import floor, ceil
from copy import copy


class Node:
    def __init__(self, value, depth, parent, children, flat_id, node_id):
        self.value = value
        self.depth = depth
        self.parent = parent
        self.children = children
        self.flat_id = flat_id
        self.node_id = node_id


def get_nodes(book, start_id=1, depth_=0):
    global nodes, flat_id
    for id_, chapter in enumerate(book):
        node_id = start_id + id_
        parent_id = (node_id - 1) // 2
        node_ = Node(value=chapter, depth=depth_, parent=parent_id, children=[], flat_id=None, node_id=node_id)
        nodes[parent_id].children.append(node_id)
        nodes[node_id] = node_
        if isinstance(chapter, list):
            get_nodes(chapter, (node_id * 2) + 1, depth_ + 1)
        else:
            nodes[node_id].flat_id = flat_id
            flat_id += 1


def remove_node(node_):
    global nodes
    for node2 in nodes[node_.parent].children:
        nodes.pop(node2)
    nodes[node_.parent].children = []
    nodes[node_.parent].value = 0


def get_next_node_id(node_id):
    global nodes
    node_id = node_id + 1
    if node_id in nodes:
        while nodes[node_id].children != []:
            node_id = node_id * 2 + 1
    while node_id not in nodes:
        node_id = node_id // 2

    return node_id


def get_last_node_id(node_id):
    global nodes
    node_id = node_id - 1
    if node_id in nodes:
        while nodes[node_id].children != []:
            node_id = node_id * 2 + 2
    while node_id not in nodes:
        node_id = (node_id - 1) // 2

    return node_id


def reset_flat_ids(node_):
    global nodes, flat_id
    if node_.children == []:
        nodes[node_.node_id].flat_id = flat_id
        flat_id += 1
    else:
        node1 = nodes[node_.children[0]]
        reset_flat_ids(node1)
        node2 = nodes[node_.children[1]]
        reset_flat_ids(node2)


def explode(node_, n_nodes):
    global nodes, flat_id
    if node_.flat_id != n_nodes - 2:
        nextnode_id = get_next_node_id(node_.node_id + 1)
        nodes[nextnode_id].value += nodes[node_.node_id + 1].value
    if node_.flat_id != 0:
        lastnode_id = get_last_node_id(node_.node_id)
        nodes[lastnode_id].value += node_.value

    remove_node(node_)
    flat_id = 0
    reset_flat_ids(nodes[0])


def split(node_):
    global nodes, flat_id
    elem = node_.value / 2
    new_val1 = floor(elem)
    new_val2 = ceil(elem)
    new_id1 = node_.node_id * 2 + 1
    new_id2 = node_.node_id * 2 + 2

    nodes[new_id1] = Node(
        value=new_val1, depth=node_.depth + 1, parent=node_.node_id, children=[], flat_id=None, node_id=new_id1
    )
    nodes[new_id2] = Node(
        value=new_val2, depth=node_.depth + 1, parent=node_.node_id, children=[], flat_id=None, node_id=new_id2
    )

    nodes[node_.node_id].children = [new_id1, new_id2]
    nodes[node_.node_id].flat_id = None

    flat_id = 0
    reset_flat_ids(nodes[0])


def build_list(nodes):
    node_ids = [node.node_id for node in nodes.values()]
    node_ids.sort(reverse=True)
    for node_id in node_ids:
        if nodes[node_id].children != []:
            nodes[node_id].value = [nodes[nodes[node_id].children[0]].value, nodes[nodes[node_id].children[1]].value]

    return nodes[0].value


def init_nodes(book):
    global nodes, flat_id
    nodes.clear()
    nodes[0] = Node(value=book, depth=0, parent=-1, children=[], flat_id=None, node_id=0)
    flat_id = 0
    get_nodes(book)
    n_nodes = len([x.node_id for x in nodes.values() if x.children == []])
    return n_nodes


def reduce_book(chapter1, chapter2):
    global nodes, flat_id

    book = copy(chapter1)
    book.append(copy(chapter2))

    n_nodes = init_nodes(book)

    found_ = True
    while found_ == True:
        found_ = False
        base_nodes = [x for _, x in nodes.items() if x.flat_id is not None]
        base_nodes.sort(key=lambda x: x.flat_id)
        for id_, node_ in enumerate(base_nodes):
            if (
                (node_.depth >= 4)
                and (node_.children == [])
                and (base_nodes[id_ + 1].children == [])
                and (base_nodes[id_ + 1].depth == node_.depth)
            ):
                explode(node_, n_nodes)
                n_nodes -= 1
                found_ = True
                break
        if found_ == False:
            for id_, node_ in enumerate(base_nodes):
                if node_.value >= 10:
                    split(node_)
                    n_nodes += 1
                    found_ = True
                    break

    built = build_list(nodes)
    return nodes, built


def sum_snails(nodes_):
    global mag
    for id_, node_ in enumerate(nodes_):
        if id_ == 0:
            if isinstance(node_, list):
                val1 = sum_snails(node_) * 3
            else:
                val1 = node_ * 3
        elif id_ == 1:
            if isinstance(node_, list):
                val2 = sum_snails(node_) * 2
            else:
                val2 = node_ * 2
        else:
            print("big_problem")
    return val1 + val2


input_ = open("day18_input")
book = []
original_numbers = []

for z, line_ in enumerate(input_):
    obj = literal_eval(line_)
    original_numbers.append(copy(obj))

nodes = {}
built = original_numbers[0]

for x in original_numbers[1:]:
    num1 = copy([built])
    num2 = copy(x)
    print(num1, num2)
    nodes, built = reduce_book(num1, num2)
    print(built)

mag = sum_snails(built)

print("part1", mag)

from itertools import permutations

num_ids = list(range(len(original_numbers)))
num_perms = list(permutations(num_ids, 2))

max_mag = 0
z = 0
for (id1, id2) in num_perms:
    z += 1
    num1 = copy([original_numbers[id1]])
    num2 = copy(original_numbers[id2])
    nodes, built = reduce_book(num1, num2)
    mag = sum_snails(built)
    if mag > max_mag:
        max_mag = mag
        print(z, max_mag)

    if z % 1000 == 0:
        print(z)

