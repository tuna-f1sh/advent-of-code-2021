from inputs import get_input

from collections import Counter, namedtuple

Point = namedtuple('Point', ['x', 'y'])

def count_lines(dinput, diagonals=False):
    """
    >>> example = get_input(5, example=True)
    >>> count_lines(example)
    5
    >>> count_lines(example, diagonals=True)
    12
    """
    count = Counter()

    for l in dinput:
        # points
        ps = l.split(" -> ")
        # point cords
        p1, p2 = Point(*map(int, ps[0].split(','))), Point(
            *map(int, ps[1].split(',')))

        # horizontal line
        if p1.x == p2.x:
            for y in range(min((p1.y, p2.y)), max((p1.y, p2.y)) + 1):
                count.update([Point(p1.x, y)])

        # vertical line
        elif p1.y == p2.y:
            for x in range(min((p1.x, p2.x)), max((p1.x, p2.x)) + 1):
                count.update([Point(x, p1.y)])

        # diagonals at exactly 45 deg allows simple range scan
        elif diagonals:
            xs = range(p1.x, p2.x + 1) if p1.x < p2.x else range(p1.x, p2.x - 1, -1)
            ys = range(p1.y, p2.y + 1) if p1.y < p2.y else range(p1.y, p2.y - 1, -1)

            # iterate through points in both ranges
            for x, y in zip(xs, ys):
                count.update([Point(x, y)])

    # return sum of two lines overlapping; count of point > 1
    return sum([c > 1 for c in count.values()])

dinput = get_input(5)

print(f"Part 1 result: {count_lines(dinput)}")
print(f"Part 2 result: {count_lines(dinput, diagonals=True)}")
