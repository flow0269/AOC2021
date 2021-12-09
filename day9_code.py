from aocd.models import Puzzle

puzzle = Puzzle(2021, 9)
input_ = puzzle.input_data.splitlines()

# input_ = open("day9_test").read().splitlines()

grid_ = [[int(x) for x in y] for y in input_]

# create a column of 10s at the left and right of the grid to allow gradients to be computed
grid_.insert(0, [10] * len(input_[0]))
grid_.append([10] * len(input_[0]))

# create a row of 10s at the top and bottom of the grid to allow gradients to be computed
[x.insert(0, 10) for x in grid_]
[x.append(10) for x in grid_]

y_dim = len(grid_)
x_dim = len(grid_[0])

# part1
low_points = []
levels = []
for y in list(range(y_dim))[1:-1]:
    for x in list(range(x_dim))[1:-1]:
        deltas = ((0, 1), (0, -1), (1, 0), (-1, 0))
        found_ = True
        for dx in deltas:
            if grid_[y + dx[1]][x + dx[0]] <= grid_[y][x]:
                found_ = False
                break
        if found_:
            levels.append(grid_[y][x] + 1)
            low_points.append((y, x))


print(sum(levels))


# recursive formula to find all basin members for part 2
def find_basin_neighbors(y_low, x_low, basin_points):
    neighbor_points = [
        (y_low - 1, x_low),
        (y_low, x_low + 1),
        (y_low + 1, x_low),
        (y_low, x_low - 1),
    ]
    neighbor_basin = [(y,x) for y, x in neighbor_points if grid_[y][x] < 9]

    for y_new, x_new in neighbor_basin:
        n_pts = len(basin_points)
        basin_points.add((y_new, x_new))
        if len(basin_points) > n_pts:
            find_basin_neighbors(y_new, x_new, basin_points)

    return n_pts


# part2
basin_sizes = []
for y_low, x_low in low_points:
    basin_points = set({(y_low, x_low)})
    basin_sizes.append(find_basin_neighbors(y_low, x_low, basin_points))

basin_sizes.sort()

print(basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])
