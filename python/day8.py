import itertools
from inputs import get_input, timing

def parse_input(dinput):
    return [(x[0].strip().split(), x[1].strip().split()) for x in [line.split('|') for line in dinput]]

def part1(parsed):
    """
    Just looks for sequence of length which is unique and returns count

    >>> parsed = parse_input(get_input(8, example=True))
    >>> part1(parsed)
    26
    """
    outputs = [x for _, x in parsed]

    unique_len = {2, 3, 4, 7}
    ret = 0

    for out in outputs:
        for seg in out:
            if len(seg) in unique_len:
                ret += 1

    return ret

def part2(parsed):
    """
    Inspired by Reddit post whilst solving my own (much more complicated!) solution. Does the same as SegmentNumber class solve but with fixed len values rather than auto - makes for simplier but less dynamic solution

    >>> parsed = parse_input(get_input(8, example=True))
    >>> part2(parsed)
    61229
    """

    sum_outputs = 0

    for i, o in parsed:
        # dict key length of input string and then set of string for wire mask
        len_mask = {len(s): set(s) for s in i}

        # append number as we iterate through string segmetns to keep base10 position
        n = ''

        for s in map(set, o):
            # compare length of string and then length of string masked with digit 4 (only with len(4)) digit 1 (only with len(2)); the overlap length (masked value) is unique and can be used as ID
            match len(s), len(s & len_mask[4]), len(s & len_mask[2]):
                case 2,_,_: n += '1' # unique
                case 3,_,_: n += '7' # unique
                case 4,_,_: n += '4' # unique
                case 7,_,_: n += '8' # unique
                case 5,2,_: n += '2'
                case 5,3,1: n += '5'
                case 5,3,2: n += '3'
                case 6,4,_: n += '9'
                case 6,3,1: n += '6'
                case 6,3,2: n += '0'

        # now convert to int and add to rolling sum
        sum_outputs += int(n)

    return sum_outputs

class SevenSegment:
    wires = {'a', 'b', 'c', 'd', 'e', 'g', 'f'}

    def __init__(self):
        # start with all wires mapped to each segment since we don't know
        self.mapping = {s: self.wires.copy() for s in self.wires}

    def __repr__(self):
        return f"SevenSegment: {self}"

    def __str__(self):
        return str(self.mapping)

    def mapped(self, segment):
        return len(self.mapping[segment]) == 1

    @property
    def solved(self):
        # when each mapping key has only 1 wire mapped
        return all(map(self.mapped, self.mapping.keys()))

    def solve_mapping(self, numbers):
        # sort numbers by len of wires, lowest first to eliminate most options quickly
        numbers = sorted(numbers, key=lambda n: len(n.wiring), reverse=False)

        while not self.solved:
            # for each segment
            for segment in self.mapping:
                # skip mapped
                if self.mapped(segment):
                    continue

                for number in numbers:
                    # if number has segment, mask with number wiring as it must include these
                    # breakpoint()
                    if segment in number.segment_map:
                        self.mapping[segment] &= number.wiring
                    # else remove them as it cannot
                    else:
                        self.mapping[segment] -= number.wiring

                    # break if mapped
                    if self.mapped(segment):
                        break

                # eliminate mapped from to be mapped
                for s, wire in self.mapping.items():
                    # remove wires that we know are mapped
                    if self.mapped(s) and segment != s:
                        self.mapping[segment] -= wire

class SegmentNumber:
    def __init__(self, number, segment_map, unique=False):
        self.number = number
        self.segment_map = segment_map
        # number of wires connecting
        self.wire_number = len(segment_map)
        self.unique = unique
        self.possible_wiring = list()

    def __repr__(self):
        return f"SegmentNumber: {self.number}: {self.possible_wiring}"

    def __str__(self):
        return str(self.number)

    @property
    def solved(self):
        return len(self.possible_wiring) == 1

    @property
    def wiring(self):
        if not self.solved:
            raise RuntimeError("Number not solved!")

        return self.possible_wiring[0]

    def process_possible(self, inputs):
        """
        Process the possible wires connecting for the number given input
        """
        # possible combos are those of len required for this number
        sets = [set(i) for i in inputs]
        self.possible_wiring = list(itertools.compress(sets, map(lambda x: len(x) == self.wire_number, sets)))

    def overlapping(self, numbers):
        """
        Returns numbers with overlapping segments
        """
        return [itertools.compress(numbers, [len(number.segment_map & self.segment_map) > 0 for number in numbers])]

    def solve_possible(self, numbers):
        # make a copy of possible to drop not possible whilst iterating on possible_wiring
        possible = self.possible_wiring.copy()

        # for each solved, mask with possible, check len of overlapping if equal, it's still possible
        for pos in self.possible_wiring:

            for number in numbers:
                # on those found only but not just unique allows us to use already solved
                if number.solved:
                    # if len of possible masked with other number wiring doesn't match len of overlapping wiring, it can't be possible
                    if len(pos & number.wiring) != len(number.segment_map & self.segment_map):
                        possible.remove(pos)
                        break

            # break if only one kept
            if len(possible) == 1:
                break

        if len(possible) == 1:
            self.possible_wiring = possible
        else:
            raise RuntimeError("Unable to solve with available numbers")

def get_segment_numbers():
    # numbers in a 7-segment display and wire count required
    return [
            SegmentNumber(0, SevenSegment.wires - {'d'}),
            SegmentNumber(1, {'c', 'f'}, unique=True),
            SegmentNumber(2, SevenSegment.wires - {'b', 'f'}),
            SegmentNumber(3, SevenSegment.wires - {'b', 'e'}),
            SegmentNumber(4, SevenSegment.wires - {'a', 'e', 'g'}, unique=True),
            SegmentNumber(5, SevenSegment.wires - {'c', 'e'}),
            SegmentNumber(6, SevenSegment.wires - {'c'}),
            SegmentNumber(7, {'a', 'c', 'f'}, unique=True),
            SegmentNumber(8, SevenSegment.wires, unique=True),
            SegmentNumber(9, SevenSegment.wires - {'e'}),
            ]

def decode_line(input_numbers):
        numbers = get_segment_numbers()

        # process numbers from input
        for number in numbers:
            number.process_possible(input_numbers)

        # then solve once we have all
        for number in numbers:
            number.solve_possible(numbers)

        # now solve seven segment wiring
        sseg = SevenSegment()
        sseg.solve_mapping(numbers)

        return numbers, sseg

def solve_line(numbers, output_numbers):
    total = ''

    for ostr in output_numbers:
        oset = set(ostr)
        for num in numbers:
            if num.wiring == oset:
                total += str(num)
                break

    return int(total)


def solve(dinput):
    """
    >>> solve(get_input(8, example=True))
    61229
    """
    parsed = parse_input(dinput)
    total = 0

    for i, o in parsed:
        numbers, _ = decode_line(i)
        total += solve_line(numbers, o)

    return total

if __name__ == "__main__":
    dinput = get_input(8)

    print(f"Part 1 result: {part1(parse_input(dinput))}")
    print(f"Part 2 result: {solve(dinput)}")
