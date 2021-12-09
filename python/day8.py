import itertools
from inputs import get_input

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

    sum_outputs = 0

    for i, o in parsed:
        # dict key length of input string and then set of string for wire mask
        len_mask = {len(s): set(s) for s in i}
        print(len_mask)

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

class SevenSegent:
    wires = {'a', 'b', 'c', 'd', 'e', 'g', 'f'}
    def __init__(self):
        # start with all wires mapped to each segment since we don't know
        self.mapping = {s: self.wires for s in self.wires}

    def mapped(self, segment):
        return len(self.mapping[segment]) == 1

    @property
    def solved(self):
        # when each mapping key has only 1 wire mapped
        return all(map(self.mapped, self.mapping.keys()))

class SegmentNumber:
    def __init__(self, number, segment_map, unique=False):
        self.number = number
        self.segment_map = segment_map
        # number of wires connecting
        self.wire_number = len(segment_map)
        self.unique = unique
        self.possible = set()
        self.found = False

    def process_possible(self, inputs):
        """
        Process the possible wires connecting for the number given input
        """
        # possible combos are those of len required for this number
        possible_combo = list(itertools.compress(inputs, map(lambda x: len(x) == self.wire_number, inputs)))

        # create a set of possible wires by concat possible combos into set to get just wires that might connect segment
        self.possible = set(''.join(possible_combo))

        # check if found when length of possible == wires required - this should always be true for unique numbers
        if len(self.possible) == self.wire_number:
            self.found = True
        else:
            self.found = False

seven_seg = SevenSegent()
# numbers in a 7-segment display and wire count required
segment_numbers = [
        SegmentNumber(0, seven_seg.wires - {'d'}),
        SegmentNumber(1, {'c', 'f'}, unique=True),
        SegmentNumber(2, seven_seg.wires - {'b', 'f'}),
        SegmentNumber(3, seven_seg.wires - {'b', 'e'}),
        SegmentNumber(4, seven_seg.wires - {'a', 'e', 'g'}, unique=True),
        SegmentNumber(5, seven_seg.wires - {'c', 'e'}),
        SegmentNumber(6, seven_seg.wires - {'c'}),
        SegmentNumber(7, {'a', 'c', 'f'}, unique=True),
        SegmentNumber(8, seven_seg.wires, unique=True),
        SegmentNumber(9, seven_seg.wires - {'e'}),
        ]

dinput = get_input(8)
parsed = parse_input(dinput)

print(f"Part 1 result: {part1(parsed)}")
print(f"Part 2 result: {part2(parsed)}")

# inputs = [i for i, _ in parsed]
# outputs = [o for _, o in parsed]

# for number in segment_numbers:
#     number.process_possible(inputs[0])

# # run until all segments have only one wire mapped
# while(not seven_seg.solved):
#     # for each segment in the display
#     for segment, wires in seven_seg.mapping.items():
#         # skip if solved
#         if seven_seg.mapped(segment):
#             continue

#         segment_numbers = itertools.compress(
#                 segment_numbers, 
#                 map(lambda n: 
#                     segment in n.segment_map and n.unique and n.found, segment_numbers
#                     ))

#         # updated the mapping based on found or unique numbers
#         for number in segment_numbers:
#             # does the number use this segment?
#             if segment in number.segment_map:
#                 breakpoint()
#                 wires &= number.possible
#                 seven_seg.mapping[segment] = wires

#     breakpoint()
