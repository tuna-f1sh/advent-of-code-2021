from typing import List
from inputs import get_input

# from collections import Counter

class LanternFish:
    # default new spawn 8 days
    def __init__(self, start_day: int = 8):
        self.day = start_day

    def update(self):
        # decrement days left until spawn
        if self.day != 0:
            self.day -= 1

            return None
        else:
            # fish timer resets to 6 because 0 is a day
            self.day = 6
            # return a new fish
            return LanternFish()

    def run_for(self, days):
        # one for ourselves
        count = 1

        # -1 because we need to run day 0
        for d in range(days-1, -1, -1):
            new = self.update()

            # recursively run the new one for the remaining days
            if new:
                count += new.run_for(d)

        return count

def model_laternfish_spawn(starting_fish: List[int], days: int = 80):
    """
    Model spawning of a school of [starting_fish] Lanternfish for [days]
    >>> example = get_input(6, example=True)
    >>> starting_fish = [*map(int, example[0].split(','))]
    >>> model_laternfish_spawn(starting_fish, 18)
    26
    >>> model_laternfish_spawn(starting_fish)
    5934
    >>> # skip this because it doesn't scale!
    >>> model_laternfish_spawn(starting_fish, days=256) # doctest: +SKIP
    26984457539
    """
    # starting fish
    fishes = [LanternFish(start_day=sd) for sd in starting_fish]

    # total in school
    count = 0

    # call each starting fish recursive function since the fish are independant
    for fish in fishes:
        count += fish.run_for(days)

    return count

def part2(starting_fish: List[int], days: int = 256, spawn_day: int = 8):
    """
    >>> example = get_input(6, example=True)
    >>> starting_fish = [*map(int, example[0].split(','))]
    >>> part2(starting_fish, days=18)
    26
    >>> part2(starting_fish, days=80)
    5934
    >>> part2(starting_fish, days=256)
    26984457539
    """
    # count ages of fish in school - only 9 possible; 0-8
    ages_count = [0] * (spawn_day + 1)

    # add in count of starting fish
    for i in starting_fish:
        ages_count[i] += 1

    # for each day
    for _ in range(0, days):
        cycle = ages_count[0]

        # get birthing fish and pop to left shift all onto next day
        cycle = ages_count.pop(0)
        # stick birthing fish back in at day 6
        ages_count[6] += cycle
        # add new fish (count of birthing fish) to day 8
        ages_count.append(cycle)

    return sum(ages_count)

dinput = get_input(6)
starting_fish = [*map(int, dinput[0].split(','))]

print(f"Part 1 result: {model_laternfish_spawn(starting_fish, days=80)}")
print(f"Part 2 result: {part2(starting_fish, days=256)}")
