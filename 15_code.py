import heapq

input_ = open("input_data\day15_input").read().splitlines()
# input_ = open("input_data\day15_test").read().splitlines()

risk_grid = [[int(x) for x in y] for y in input_]

x_range = len(risk_grid[0])
y_range = len(risk_grid)

def in_range(x,y,offset_):
    global x_range,y_range
    return (x + offset_[0] > -1) & (x + offset_[0] < x_range) & (y + offset_[1] > -1) & (y + offset_[1] < y_range)
offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

risk_dict = {(x,y):risk_grid[y][x] for x in range(x_range) for y in range(y_range)}
neighbor_dict = {(x,y):[(x + offset_[0], y + offset_[1]) for offset_ in offsets if in_range(x,y,offset_)] for x in range(x_range) for y in range(y_range) }

#using https://www.redblobgames.com/pathfinding/a-star/implementation.html for dijkstra_search
def dijkstra_search(risk_dict, target, start=(0, 0)):
    path_queue = []
    heapq.heappush(path_queue, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not len(path_queue) == 0:
        current = heapq.heappop(path_queue)[1]

        if current == target:
            break

        for neighbor_ in neighbor_dict[current]:
            new_cost = cost_so_far[current] + risk_dict[neighbor_]
            if neighbor_ not in cost_so_far or new_cost < cost_so_far[neighbor_]:
                cost_so_far[neighbor_] = new_cost
                priority = new_cost
                heapq.heappush(path_queue, (priority, neighbor_))
                came_from[neighbor_] = current

    return came_from, cost_so_far


def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    path.append(start_node)

    return shortest_path[target_node], reversed(path)


target_node = (x_range - 1, y_range - 1)
previous_nodes, shortest_path = dijkstra_search(risk_dict, target_node)
n_steps, shortest_path = print_result(previous_nodes, shortest_path, (0, 0), target_node)

print("part1", n_steps)

