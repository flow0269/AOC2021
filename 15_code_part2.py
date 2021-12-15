import heapq

input_ = open("input_data\day15_input").read().splitlines()
# input_ = open("input_data\day15_test").read().splitlines()

risk_grid = [[int(x) for x in y] for y in input_]
n_rows = len(risk_grid)
grid_o = {}

grid_o[0] = risk_grid
for off_ in range(1, 9):
    grid_o[off_] = [[((x + off_ - 1) % 9) + 1 for x in y] for y in risk_grid]

def grid_large_row(y):
    global grid_o,n_rows
    return [
        grid_o[y][x] + grid_o[y+1][x] + grid_o[y+2][x] + grid_o[y+3][x] + grid_o[y+4][x]
        for x in range(n_rows)
    ]

mega_grid = grid_large_row(0)
mega_grid.extend(grid_large_row(1))
mega_grid.extend(grid_large_row(2))
mega_grid.extend(grid_large_row(3))
mega_grid.extend(grid_large_row(4))

x_range = len(mega_grid[0])
y_range = len(mega_grid)

def in_range(x,y,offset_):
    global x_range,y_range
    return (x + offset_[0] > -1) & (x + offset_[0] < x_range) & (y + offset_[1] > -1) & (y + offset_[1] < y_range)
offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

risk_dict = {(x,y):mega_grid[y][x] for x in range(x_range) for y in range(y_range)}
neighbor_dict = {(x,y):[(x + offset_[0], y + offset_[1]) for offset_ in offsets if in_range(x,y,offset_)] for x in range(x_range) for y in range(y_range) }
print(x_range, y_range)

#using https://www.redblobgames.com/pathfinding/a-star/implementation.html for dijkstra_search
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