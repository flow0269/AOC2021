input_ = open("day11_input").read().splitlines()

grid_ = [[int(y) for y in x] for x in input_]
offsets = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def in_bounds(y, x, o):
    if (y + o[0] < len(grid_)) & (y + o[0] > -1) & (x + o[1] < len(grid_[0])) & (x + o[1] > -1):
        return True
    else:
        return False


def light_offsets(y, x, grid_, zeroed, total_flashes):
    global offsets
    for o in offsets:
        if in_bounds(y, x, o):
            if (y + o[0], x + o[1]) not in zeroed:
                grid_[y + o[0]][x + o[1]] = (grid_[y + o[0]][x + o[1]] + 1) % 10

                if grid_[y + o[0]][x + o[1]] == 0:
                    total_flashes.append(1)
                    zeroed.add((y + o[0], x + o[1]))
                    light_offsets(y + o[0], x + o[1], grid_, zeroed, total_flashes)


def increment(grid_, zeroed, total_flashes):
    for y, row in enumerate(grid_):
        for x, val in enumerate(row):
            if (y, x) not in zeroed:
                grid_[y][x] = (val + 1) % 10
                if grid_[y][x] == 0:
                    total_flashes.append(1)
                    zeroed.add((y, x))
                    light_offsets(y, x, grid_, zeroed, total_flashes)
    return grid_


zeroed = set()
total_flashes = []
for iteration_number in range(1000):
    zeroed.clear()
    grid_ = increment(grid_, zeroed, total_flashes)
    if iteration_number == 99:
        print("part1 answer", len(total_flashes))
    if len(zeroed) == len(grid_) * len(grid_[0]):
        break

print("part2 answer", iteration_number + 1)

