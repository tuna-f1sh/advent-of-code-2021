from typing import List

from inputs import get_ints

def count_increasing(locations: List[int]):
    """
    >>> example = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    >>> count_increasing(example)
    7
    """
    return sum([x > y for x, y in zip(locations[1:], locations)])

def count_window(locations: List[int], window_size: int = 3):
    """
    >>> example = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    >>> count_window(example)
    5
    """

    # can skip 1,2 because A = (A+B+C - (B+C)) - (B+C+D - (B+C)) = D
    return sum([x > y for x, y in zip(locations[window_size:], locations)])

def count_window_alt(locations: List[int], window_size: int = 3):
    """
    >>> example = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    >>> count_window_alt(example)
    5
    """

    return sum([x-y > 0 for x, y in zip(locations[window_size:], locations)])

part1 = get_ints(1)

print(f"Part 1 result: {count_increasing(part1)}")
print(f"Part 2 result: {count_window(part1)}")
