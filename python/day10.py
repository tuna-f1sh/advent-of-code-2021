from inputs import *

from collections import Counter

# thought about using ascii +1 but they are not next to each other so a dict instead
CHAR_PAIRS = {
    "[": "]",
    "(": ")",
    "{": "}",
    "<": ">",
}

ILLEGAL_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

def find_closing(char, line):
    ret = 0

    if char not in CHAR_PAIRS:
        raise ValueError()

    for i, c in enumerate(line):
        print(f"looking at {c}")

        # if we find closing break
        if c == CHAR_PAIRS[char]:
            return 0
        # is it another (invalid) closing?
        elif c in CHAR_PAIRS.values():
            return ILLEGAL_POINTS[c]
        # else must be opening so run recursive
        else:
            ret += find_closing(c, line[i+1:])

    return ret

def syntax_checker(dinput):
    """
    Checks lines in dinput for first syntax error and returns sum of syntax error score

    >>> dinput = get_input(10, example=True)
    >>> syntax_checker(dinput)
    26397

    """
    checker_score = 0

    for line in dinput:
        opening = [line[0]]

        for c in line:

            # updating opening if opening char
            if c in CHAR_PAIRS:
                opening.append(c)
            # if closed, pop opening
            elif c == CHAR_PAIRS[opening[-1]]:
                opening.pop()
            elif c in CHAR_PAIRS.values():
                checker_score += ILLEGAL_POINTS[c]
                break

    return checker_score

dinput = get_input(10)

print(f"Part 1 result: {syntax_checker(dinput)}")
