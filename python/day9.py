from inputs import get_input

dinput = get_input(9)
matrix = [[int(c) for c in line] for line in dinput]

def find_low_points(matrix):
    """
    >>> dinput = get_input(9, example=True)
    >>> matrix = [[int(c) for c in line] for line in dinput]
    >>> find_low_points(matrix)
    15
    """
    total_sum = 0

    def nearest(point):
        ret = []
        i, j = point
        rl = len(matrix[0])
        cl = len(matrix)

        if i > 0:
            ret.append(matrix[i-1][j])
        if i + 1 < cl:
            ret.append(matrix[i+1][j])

        if j > 0:
            ret.append(matrix[i][j-1])
        if j + 1 < rl:
            ret.append(matrix[i][j+1])

        return ret

    for i, row in enumerate(matrix):
        total_sum += sum(height+1 if all(map(lambda n: height < n, nearest((i,j)))) else 0 for j, height in enumerate(row))

    return total_sum

def find_basins(matrix):
    """
    >>> dinput = get_input(9, example=True)
    >>> matrix = [[int(c) for c in line] for line in dinput]
    >>> find_basins(matrix)
    1134
    """
    # different to part one in that it returns cords not height
    def nearest(point):
        ret = []
        i, j = point
        rl = len(matrix[0])
        cl = len(matrix)

        if i > 0:
            ret.append((i-1, j))
        if i + 1 < cl:
            ret.append((i+1, j))

        if j > 0:
            ret.append((i, j-1))
        if j + 1 < rl:
            ret.append((i, j+1))

        return ret

    def get_basin(point):
        # set of cord
        basin = {point}

        for i, j in nearest(point):
            if matrix[point[0]][point[1]] < matrix[i][j] < 9:
                basin |= get_basin((i, j))

        return basin

    low_points = []

    for i, row in enumerate(matrix):
        for j, height in enumerate(row):
            if all(map(lambda n: height < matrix[n[0]][n[1]], nearest((i,j)))):
                low_points.append((i, j))

    basin_sizes = sorted([len(get_basin((i, j))) for i, j in low_points])

    # largest 3
    return basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1]

print(f"Part 1 result: {find_low_points(matrix)}")

print(f"Part 2 result: {find_basins(matrix)}")
