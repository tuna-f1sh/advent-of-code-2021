from typing import List

from inputs import get_input

class Submarine():
    """
    >>> example = get_input(2, example=True)
    >>> sub = Submarine()
    >>> sub.read_course(example)
    >>> sub.horizontal * sub.depth
    150

    """
    def __init__(self, horizontal: int = 0, depth: int = 0):
        self.depth = depth
        self.horizontal = horizontal

    def action(self, direction: str, distance: int):
        if direction == "forward":
            self.horizontal += distance
        elif direction == "backward":
            self.horizontal -= distance
        elif direction == "up":
            self.depth -= distance
        elif direction == "down":
            self.depth += distance
        else:
            raise ValueError("Invalid direction!")

    def read_course(self, course: List[str]):
        for line in course:
            direction, distance = line.split()
            distance = int(distance)

            self.action(direction, distance)

class SubmarineAim(Submarine):
    """
    >>> example = get_input(2, example=True)
    >>> sub = SubmarineAim()
    >>> sub.read_course(example)
    >>> sub.horizontal * sub.depth
    900
    """

    def __init__(self, horizontal: int = 0, depth: int = 0, aim: int = 0):
        super().__init__(horizontal=horizontal, depth=depth)
        self.aim = aim

    def action(self, direction: str, distance: int):
        if direction == "forward":
            self.horizontal += distance
            self.depth += (distance * self.aim)
        elif direction == "backward":
            self.horizontal -= distance
            self.depth -= (distance * self.aim) * -1
        elif direction == "up":
            self.aim -= distance
        elif direction == "down":
            self.aim += distance
        else:
            raise ValueError("Invalid direction!")

part1 = get_input(2)
sub = Submarine()
sub.read_course(part1)

sub2 = SubmarineAim()
sub2.read_course(part1)

print(f"Part 1 result: {sub.horizontal * sub.depth}")
print(f"Part 2 result: {sub2.horizontal * sub2.depth}")
