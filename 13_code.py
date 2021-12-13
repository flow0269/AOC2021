input_ = open("day13_input").read().splitlines()
# input_ = open("day13_test").read().splitlines()

input_split = [[x for x in y.split(",")] for y in input_]

coord_index = input_split.index([""])
grid_coords = [(int(x[0]), int(x[1])) for x in input_split[:coord_index]]
fold_instructs = [x[0][11:].split("=") for x in input_split[coord_index + 1 :]]

x_range = max([x[0] for x in grid_coords]) + 1
y_range = max([x[1] for x in grid_coords]) + 1
print(x_range, y_range)

grid_ = [[0 for x in range(x_range)] for y in range(y_range)]
for x, y in grid_coords:
    grid_[y][x] = 1


def flip_grid(flip_direction, flip_loc, grid_):
    x_range = len(grid_[0])
    y_range = len(grid_)
    if flip_direction == "y":
        grid1 = grid_[:flip_loc]
        grid2 = grid_[flip_loc + 1 :]

        grid2_T = list(zip(*grid2))
        grid2_T_flip = [list(reversed(grid2_T[x])) for x in range(x_range)]
        grid2_flip = [list(x) for x in list(zip(*grid2_T_flip))]
        return grid1, grid2_flip
    else:
        grid1 = [grid_[x][:flip_loc] for x in range(y_range)]
        grid2 = [grid_[x][flip_loc + 1 :] for x in range(y_range)]
        grid2_flip = [list(reversed(x)) for x in grid2]
        return grid1, grid2_flip


def sum_grids(grid1, grid2):
    for y in range(len(grid1)):
        for x in range(len(grid1[0])):
            grid1[y][x] = min(grid1[y][x] + grid2[y][x], 1)

    return grid1


for iteration, fold_ in enumerate(fold_instructs):
    grid1, grid2_flip = flip_grid(fold_[0], int(fold_[1]), grid_)

    grid_ = sum_grids(grid1, grid2_flip)
    if iteration == 0:
        print("part1", sum([sum(x) for x in grid_]))

stop_here = 1  # answer is spelled out by final grid

