import math
import statistics

from inputs import get_input


dinput = get_input(7, example=True)
ships = [*map(int, dinput[0].split(','))]

def find_brute_optimum_start(ships, costfn=lambda x: x):
    """
    Finds using brute force calculation of all costs then min

    >>> dinput = get_input(7, example=True)
    >>> ships = [*map(int, dinput[0].split(','))]
    >>> find_brute_optimum_start(ships)
    37
    >>> find_brute_optimum_start(ships, costfn=lambda x: x * (x+1) // 2)
    168
    """
    options = [*range(min(ships), max(ships) + 1)]
    distances_to_horizontal = [sum(costfn(abs(x - i)) for x in ships) for i in options]

    return min(distances_to_horizontal)

def solve_min(ships, statfn=statistics.median, costfn=lambda x: x):
    """
    Solver for finding optimum starting position
    """
    # mean for cost function will be least expensive
    stat = statfn(ships)
    # we are bound to int so need to check floor and ceil
    stats = (math.floor(stat), math.ceil(stat))

    return min(sum(costfn(abs(s-m)) for s in ships) for m in stats)

def find_optimum_start_linear(ships):
    """
    >>> dinput = get_input(7, example=True)
    >>> ships = [*map(int, dinput[0].split(','))]
    >>> find_optimum_start_linear(ships)
    37
    """
    # use middle value (median) of ships as the start as this will be the shortest distance to all
    return solve_min(ships, statfn=statistics.median)

def find_optimum_start_nonconst(ships):
    """
    >>> dinput = get_input(7, example=True)
    >>> ships = [*map(int, dinput[0].split(','))]
    >>> find_optimum_start_nonconst(ships)
    168
    """
    # with non-constant change, mean value will be least cost start
    return solve_min(ships, statfn=statistics.mean, costfn=lambda x: x * (x+1) // 2)

example = find_optimum_start_linear(ships)

dinput = get_input(7)
ships = [*map(int, dinput[0].split(','))]

part1 = find_optimum_start_linear(ships)
print(f"Part 1 result: {part1}")

part2 = find_optimum_start_nonconst(ships)
print(f"Part 2 result: {part2}")
