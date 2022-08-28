from tkinter import W
from PIL import Image
import numpy as np
import mcpi.minecraft as minecraft
import mcpi.entity as entity
import mcpi.block as block
import random
import math
from . import util
import time


def draw_map(mc, l0=10, hmax=10, base_gray=100, image='cave_system.png'):
    im = Image.open(image)
    pix = im.load()

    mc.setBlocks(0, -256, 0,
                 im.size[0], l0+(hmax-1)+1, im.size[1], block.LAVA)
    util.msg(mc, 'Standby, burning entities to death...')
    time.sleep(15)

    # mc.setBlocks(0, -256, 0,
    #             im.size[0], l0+(hmax-1)+1, im.size[1], block.AIR)
    #util.msg(mc, 'Standby, dropping entities into void...')
    # time.sleep(15)

    util.msg(mc, 'Drilling caves...')
    mc.setBlocks(0, -256, 0,
                 im.size[0], l0+(hmax-1)+1, im.size[1], block.STONE)

    # Also down-side!
    for z in np.arange(0, im.size[1]):
        for x in np.arange(0, im.size[0]):
            p = pix[x, z]
            if abs(p[0]-p[1]) <= 4 and abs(p[1]-p[2]) <= 4 and p[0] >= base_gray-2:
                h = int(hmax * (float(p[0]-base_gray)/base_gray))
                if h < 1:
                    h = 1
                mc.setBlocks(float(x), l0-(h/3), float(z), float(x),
                             l0+(h-1), float(z), block.AIR)
                if random.randint(0, 10) == 0:
                    mc.setBlock(float(x), l0+h, float(z),
                                block.GLOWSTONE_BLOCK)
            elif pix[x, z] == util.MAP_STONE:
                # Already a stone
                pass
            else:
                print('Bad pixel (%d,%d,%d,%d) at %d,%d' % (*p, x, z))
