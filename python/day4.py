from inputs import get_input

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

class Board:
    def __init__(self, grid_strs):
        # make grid with list rows
        self.grid = [[int(x) for x in line.strip().split()] for line in grid_strs]
        # then set rows
        self.set_rows = [set(x) for x in self.grid]
        # create tranpose for comparing column matches
        self.set_cols = [*map(set, zip(*self.grid))]

    def is_match(self, numbers: set):
        """
        Checks for match by masking with number set, each row and column in the board
        """
        for row in self.set_rows:
            if row & numbers == row:
                return True

        for col in self.set_cols:
            if set(col) & numbers == col:
                return True

        return False

    @property
    def numbers(self):
        ret = set()

        for n in self.grid:
            ret.update(n)

        return ret

    def sum_nonmatching(self, numbers: set):
        """
        >>> example = get_input(4, example=True)
        >>> numbers, boards = parse_input(example)
        >>> boards[2].sum_nonmatching(set(numbers[:12]))
        188
        """
        # we only need to do this in one transpose
        # eor numbers with row so only exclusively in row
        return sum([sum((row ^ numbers) & row) for row in self.set_rows])

def parse_input(dinput):
    numbers = [*map(int, dinput[0].split(','))]
    boards = []
    boardlines = []

    for line in dinput[2:]:

        if line != "":
            boardlines.append(line)
        else:
            boards.append(Board(boardlines))
            boardlines = []

    if boardlines:
        boards.append(Board(boardlines))

    return numbers, boards

def bingo(numbers, boards):
    """
    >>> example = get_input(4, example=True)
    >>> numbers, boards = parse_input(example)
    >>> bingo(numbers, boards)
    4512
    """

    # iterate through numbers calling one at a time to increase sequence until we find a winner
    for i, num in enumerate(numbers):

        # go through boards checking for a match
        for b in boards:
            sequence = set(numbers[:i+1])

            # is sequence is a match, calculate the result
            if b.is_match(sequence):
                sumnm = b.sum_nonmatching(sequence)

                # remove winner for p2
                boards.remove(b)

                # entry wants the sum of non-matching * number called
                return sumnm * num

dinput = get_input(4)
numbers, boards = parse_input(dinput)

print(f"Part 1 result: {bingo(numbers,boards)}")

# run until all boards have bingoed, last result is last winner - note will empy boards global
while boards:
    p2 = bingo(numbers, boards)

print(f"Part 2 result: {p2}")
