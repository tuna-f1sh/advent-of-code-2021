import time
import random

from inputs import get_input
from day8 import *

from microdotphat import set_pixel, clear, show, write_char

# Each hex number is a column, each bit in the number is a row in that column. Least significant bit is the topmost row.
segments = {
        'a': [0x00, 0x01, 0x01, 0x01, 0x00], #  aaa
        'b': [0x06, 0x00, 0x00, 0x00, 0x00], # b   c
        'c': [0x00, 0x00, 0x00, 0x00, 0x06], # b   c
        'd': [0x00, 0x08, 0x08, 0x08, 0x00], #  ddd
        'e': [0x30, 0x00, 0x00, 0x00, 0x00], # e   f
        'f': [0x00, 0x00, 0x00, 0x00, 0x30], # e   f
        'g': [0x00, 0x40, 0x40, 0x40, 0x00], #  ggg
        'x': [0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        }

def _set_segment(segment, setting, offset_x=0, offset_y=0):
    char = segments[segment]

    for x in range(5):
        for y in range(7):
            p = (char[x] & (1 << y))
            if p:
                set_pixel(offset_x + x, offset_y + y, p and setting)

def set_segment(segment, setting, unit):
    _set_segment(segment, setting, offset_x=unit*8, offset_y=0)

def show_number(segments, unit):
    for seg in segments:
        set_segment(seg, 1, unit)

def test():
    for seg in segments.keys():
        set_segment(seg, 1, 0)
        set_segment(seg, 1, 2)
        write_char(seg, offset_x=8, offset_y=0)
        show()
        time.sleep(0.5)

def solve_line(numbers, output_numbers):
    total = ''

    # display them all to start
    for i, ostr in enumerate(output_numbers):
        oset = set(ostr)

        show_number(oset, i+2)
        show()

    # now show solution one by one
    for i, ostr in enumerate(output_numbers):
        oset = set(ostr)

        for num in numbers:
            if num.wiring == oset:
                if num.wiring != num.segment_map:
                    set_segment('x', 0, i+2)
                    show_number(num.segment_map, i+2)
                    show()
                    time.sleep(random.randint(2,20) / 100)

                total += str(num)
                break

    return int(total)

def solve(dinput):
    parsed = parse_input(dinput)
    total = 0
    rotate_seg = ['d', 'f', 'g', 'e']
    rotate_pos = 0
    rotate_toggle = True
    clear()

    for i, o in parsed:
        numbers, _ = decode_line(i)
        total += solve_line(numbers, o)
        set_segment(rotate_seg[rotate_pos], rotate_toggle, 0)
        set_segment(rotate_seg[rotate_pos], rotate_toggle, 1)

        if rotate_pos < len(rotate_seg) - 1:
            rotate_pos += 1
        else:
            rotate_toggle = not rotate_toggle
            rotate_pos = 0

        time.sleep(0.20)

    return total

# test()

if __name__ == "__main__":
    dinput = get_input(8, example=True)
    result = solve(dinput)

    numbers = get_segment_numbers()
    clear()

    str_result = str(result)
    toggle = True

    for i, s in enumerate(str_result):
        write_char('=')
        show_number(numbers[int(s)].segment_map, 6 - len(str_result) + i)

    for _ in range(8):
        if toggle:
            write_char('=')
        else:
            set_segment('x', 0, 0)
        toggle = not toggle

        show()
        time.sleep(0.5)
