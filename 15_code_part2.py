import heapq

input_ = open("input_data\day15_input").read().splitlines()
# input_ = open("input_data\day15_test").read().splitlines()

risk_grid = [[int(x) for x in y] for y in input_]
grid_offsets = {}

for off_ in range(1, 9):
    grid_offsets[off_] = [[((x + off_ - 1) % 9) + 1 for x in risk_grid[y]] for y in range(len(risk_grid))]


grid_ = [
    risk_grid[x] + grid_offsets[1][x] + grid_offsets[2][x] + grid_offsets[3][x] + grid_offsets[4][x]
    for x in range(len(risk_grid))
]
grid_row2 = [
    grid_offsets[1][x] + grid_offsets[2][x] + grid_offsets[3][x] + grid_offsets[4][x] + grid_offsets[5][x]
    for x in range(len(risk_grid))
]
grid_row3 = [
    grid_offsets[2][x] + grid_offsets[3][x] + grid_offsets[4][x] + grid_offsets[5][x] + grid_offsets[6][x]
    for x in range(len(risk_grid))
]
grid_row4 = [
    grid_offsets[3][x] + grid_offsets[4][x] + grid_offsets[5][x] + grid_offsets[6][x] + grid_offsets[7][x]
    for x in range(len(risk_grid))
]
grid_row5 = [
    grid_offsets[4][x] + grid_offsets[5][x] + grid_offsets[6][x] + grid_offsets[7][x] + grid_offsets[8][x]
    for x in range(len(risk_grid))
]

grid_.extend(grid_row2)
grid_.extend(grid_row3)
grid_.extend(grid_row4)
grid_.extend(grid_row5)

x_range = len(grid_[0])
y_range = len(grid_)

risk_dict = dict()
offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
neighbor_dict = dict()
for y in range(y_range):
    for x in range(x_range):
        risk_dict[(x, y)] = grid_[y][x]
        neighbor_dict[(x, y)] = [(x + offset_[0], y + offset_[1]) for offset_ in offsets if (x + offset_[0] > -1) & (x + offset_[0] < x_range) & (y + offset_[1] > -1) & (y + offset_[1] < y_range)]


print(x_range, y_range)

def dijkstra_search(risk_dict, target, start=(0, 0)):
    path_queue = []
    heapq.heappush(path_queue, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not len(path_queue)==0:
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

print("part2", n_steps)

