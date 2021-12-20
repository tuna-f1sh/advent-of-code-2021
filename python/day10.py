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

CLOSING_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

def find_closing(char, line):
    ret = 0

    if char not in CHAR_PAIRS:
        raise ValueError()

    for i, c in enumerate(line):
        print(f"looking at {c}")

        # if we find closing break
        if c == CHAR_PAIRS[char]:
            return 0, i
        # is it another (invalid) closing?
        elif c in CHAR_PAIRS.values():
            return ILLEGAL_POINTS[c], i
        # else must be opening so run recursive
        else:
            rec, i = find_closing(c, line[i+1:])
            ret += rec

    return ret, len(line) - 1 # index is last in line if here

def syntax_checker(dinput):
    """
    Checks lines in dinput for first syntax error and returns sum of syntax error score

    >>> dinput = get_input(10, example=True)
    >>> syntax_checker(dinput)
    (26397, 288957)

    """
    checker_score = 0
    closing_scores = []

    for line in dinput:
        opening = []
        corrupted = 0

        for c in line:
            # updating opening if opening char
            if c in CHAR_PAIRS:
                opening.append(c)
            # if closed, pop opening
            elif c in CHAR_PAIRS[opening[-1]]:
                opening.pop()
            elif c in CHAR_PAIRS.values():
                corrupted = ILLEGAL_POINTS[c]
                break

        if corrupted > 0:
            checker_score += corrupted
        elif len(opening) > 0:
            closing_score = 0
            # we want last in first in line so reverse
            opening.reverse()
            # after running checker on line, chars left in opening are unclosed
            closing_required = [CHAR_PAIRS[c] for c in opening]

            for closing in closing_required:
                closing_score *= 5
                closing_score += CLOSING_POINTS[closing]

            closing_scores.append(closing_score)

    closing_scores.sort()

    return checker_score, closing_scores[len(closing_scores) // 2]

dinput = get_input(10)

print(f"Part 1 result: {syntax_checker(dinput)[0]}")
print(f"Part 2 result: {syntax_checker(dinput)[1]}")
