from inputs import *

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

class Tile:
    def __init__(self, pos: Point, level: int):
        self.pos = pos
        self.level = level

    @property
    def flashing(self):
        return self.level >= 10

    def reset(self):
        if self.flashing:
            self.level = 0
        else:
            raise RuntimeError("Tile not flashing!")

    def update(self, amount=1):
        """
        Updates level and returns if update caused to flash
        """
        # if not flashing already
        if not self.flashing:

            # increment level if not > 9
            if (self.level + amount) <= 9:
                self.level += amount
            else:
                self.level = 10

                return True
        # return false as we are flashing but this update didn't cause flashing
        else:
            return False

class OctopusGrid:
    """
    >>> dinput = get_input(11, example=True)
    >>> octo_grid = OctopusGrid(dinput)
    >>> sum(octo_grid.step() for _ in range(10))
    204
    >>> octo_grid = OctopusGrid(dinput)
    >>> sum(octo_grid.step() for _ in range(100))
    1656
    >>> octo_grid = OctopusGrid(dinput)
    >>> octo_grid.find_all_flash()
    195
    """

    def __init__(self, dinput):
        tiles = []
        points = []

        # maybe a shorter way to do this...
        for y, line in enumerate(dinput):
            for x, level in enumerate(list(line)):
                points.append(Point(x,y))
                tiles.append(Tile(points[-1], int(level)))

        self.grid = dict(zip(points,tiles))
        self.rows = len(dinput)
        self.cols = len(dinput[0])

    def __repr__(self):
        return str(self)

    def __str__(self):
        ret = ""
        for row in self.state:
            ret += f"{row}\n"

        return ret

    @property
    def state(self):
        rows = [0] * self.rows

        for point, tile in self.grid.items():
            rows[point.y] += tile.level * 10**(self.cols - 1 - point.x)

        return rows

    def propogate(self, flashing):
        f = flashing.pos

        # update (+1) to all neighbours
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:

                # neighbour point
                p = Point(f.x+x,f.y+y)

                if p in self.grid:
                    nt = self.grid[p]

                    # recursively call with new one if we caused it to flash
                    if nt.update():
                        self.propogate(nt)

    def step(self, reset=True):
        flashing_count = 0
        flashing = []

        for tile in self.grid.values():
            # first step them all but capture flashing for next step
            if tile.update():
                flashing.append(tile)

        # recursively propogate the flashing states - independant loop after all tiles updated
        for ftile in flashing:
            self.propogate(ftile)

        # now count and reset those in flashing state - independant again as can't reset until all propogated
        for tile in self.grid.values():
            if tile.flashing:
                flashing_count += 1
                if reset: tile.reset()

        return flashing_count

    def find_all_flash(self):
        step = 0

        while (True):
            # step 0 is initialised state so step before update
            step += 1

            # if all tiles flashing, break
            if self.cols * self.rows == self.step():
                break

        return step


if __name__ == "__main__":
    dinput = get_input(11)

    octo_grid = OctopusGrid(dinput)
    print(f"Part 1 result: {sum(octo_grid.step() for _ in range(100))}")
    octo_grid = OctopusGrid(dinput)
    print(f"Part 2 result: {octo_grid.find_all_flash()}")
