import time

from PIL import ImageDraw
from flipdot import client, display

from inputs import get_input
from day11 import OctopusGrid

# 1 x 2, 28 x 7 panels in portrait
PANEL_X = 28
PANEL_Y = 7
MATRIX_SIZE_X = 1
MATRIX_SIZE_Y = 2
MATRIX_X = MATRIX_SIZE_X * PANEL_X
MATRIX_Y = MATRIX_SIZE_Y * PANEL_Y

def display_text(d, text, xy=(0,0), font=None, rotate=False):
    draw = ImageDraw.Draw(d.im)

    if rotate: d.im = d.im.rotate(angle=90, expand=1)
    draw = ImageDraw.Draw(d.im)
    d.reset()
    draw.text(xy, text, font=font)

    # now rotate the image back to display format
    if rotate: d.im = d.im.rotate(angle=-90, expand=1)
    d.send()
    del draw

def octopus_flip(steps=100, refresh=0.15):
    dinput = get_input(11)

    # FlipDot display
    disp = display.Display(MATRIX_X, MATRIX_Y, display.create_display((PANEL_X, PANEL_Y), (MATRIX_X, MATRIX_Y)))
    # disp.connect(client.SerialClient('/dev/tty.usbserial-A9IYFIPD'))
    disp.connect(client.TCPClient('192.168.8.234', 9000))
    disp.reset(white=False)
    disp.send()

    # Advent of Code
    octo_grid = OctopusGrid(dinput)
    # centering of 10x10 grid
    sx = int((28 - 10) / 2)
    sy = int((14 - 10) / 2)
    result = 0

    for _ in range(steps):
        # step but don't reset flashing so we can show on display
        result += octo_grid.step(reset=False)

        for cord, tile in octo_grid.grid.items():
            centered_cord = (cord.x+sx, cord.y+sy)
            disp.im.putpixel(centered_cord, (255, 255, 255) if tile.flashing else (0,0,0))
        # send and hold for refresh
        disp.send()
        time.sleep(refresh)

        # now reset
        for tile in octo_grid.grid.values():
            if tile.flashing:
                tile.reset()

    # display result
    disp.reset()
    display_text(disp, str(result), xy=(0, 0))
    time.sleep(refresh)

octopus_flip()
