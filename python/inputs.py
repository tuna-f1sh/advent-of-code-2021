import os
from typing import List

def get_input(day: int, example: bool = False, split: str = '\n', raw: bool = False):
    """
    Get the input for the year and day

    :param day int: day to get
    :param example bool: example file rather than real
    """
    day_str = 'day{}_example.txt' if example else 'day{}.txt'
    if raw:
        data = open(os.path.join('../input', day_str.format(day)), 'r').read()
    else:
        data = open(os.path.join('../input', day_str.format(day)), 'r').read().strip().split(split)
    return data

def get_ints(day, **kwargs):
    """
    Return list of ints from input file

    :param day int: day to get
    :param example bool: example file rather than real
    """
    data = get_input(day, **kwargs)
    return [int(x) for x in data]
