from PIL import Image
import numpy as np
import mcpi.minecraft as minecraft
import mcpi.entity as entity
import mcpi.block as block
import random
import math
from . import util
import time


def draw_map(mc, image='cave_system.png'):
    im = Image.open(image)
    pix = im.load()

    hmax = 10
    l0 = 10
    base_gray = 100
    mc.setBlocks(0, -256, 0,
                 im.size[0], l0+(hmax-1)+1, im.size[1], block.AIR)
    print('Standby, dropping entities into void...')
    time.sleep(5)
    print('Rebuilding floor...')
    mc.setBlocks(0, -256, 0,
                 im.size[0], l0+(hmax-1)+1, im.size[1], block.STONE)
    time.sleep(5)

    # Also down-side!
    for z in np.arange(0, im.size[1]):
        for x in np.arange(0, im.size[0]):
            p = pix[x, z]
            if abs(p[0]-p[1]) <= 2 and abs(p[1]-p[2]) <= 2 and p[0] >= base_gray-2:
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
