import mcpi.block as block
import numpy as np
from . import util
import random


def draw_corridor(mc, cx, cy, cz, rot=0, holes=[]):
    cx = float(cx)
    cy = float(cy)
    cz = float(cz)

    side = 9
    is_hole = {
        'x0': lambda x, y, z: x == 0 and y != 0 and y != side-1 and z != 0 and z != side-1,
        'x1': lambda x, y, z: x == side-1 and y != 0 and y != side-1 and z != 0 and z != side-1,
        'y0': lambda x, y, z: y == 0 and x != 0 and x != side-1 and z != 0 and z != side-1,
        'y1': lambda x, y, z: y == side-1 and x != 0 and x != side-1 and z != 0 and z != side-1,
        'z0': lambda x, y, z: z == 0 and y != 0 and y != side-1 and x != 0 and x != side-1,
        'z1': lambda x, y, z: z == side-1 and y != 0 and y != side-1 and x != 0 and x != side-1,
    }

    for x in np.arange(0, side, 1):
        for y in np.arange(0, side, 1):
            for z in np.arange(0, side, 1):
                mc.setBlock(cx+x, cy+y, cz+z, block.AIR)

    for x in np.arange(0, side, 1):
        for y in np.arange(0, side, 1):
            for z in np.arange(0, side, 1):
                wall = False
                if x == 0 or x == side-1 or y == 0 or y == side-1 or z == 0 or z == side-1:
                    wall = True
                for hole in holes:
                    if is_hole[hole](x, y, z):
                        wall = False
                if wall:
                    mc.setBlock(*util.to_rot(cx, cy, cz, x, y, z, rot),
                                block.STONE_BRICK)
                else:
                    if y == side-2 and random.randint(1, 4) == 1:
                        mc.setBlock(
                            *util.to_rot(cx, cy, cz, x, y, z, rot), block.COBWEB)
                    else:
                        mc.setBlock(
                            *util.to_rot(cx, cy, cz, x, y, z, rot), block.AIR)

    torch_wall = 'y0'
    torch_wall = set(set(is_hole.keys()).difference(
        set(holes))).difference(['y1', 'y0'])
    if len(torch_wall) > 0:
        torch_wall = torch_wall.pop()
    halfside = int(side/2)
    if torch_wall == 'x0':
        mc.setBlock(*util.to_rot(cx, cy, cz, 1, halfside, halfside, rot),
                    block.TORCH[0], util.to_torch_dir_rot(util.TORCH_DIR_X1, rot))
    elif torch_wall == 'x1':
        mc.setBlock(*util.to_rot(cx, cy, cz, side-2, halfside, halfside, rot),
                    block.TORCH[0], util.to_torch_dir_rot(util.TORCH_DIR_X0, rot))
    elif torch_wall == 'z0':
        mc.setBlock(*util.to_rot(cx, cy, cz, halfside, halfside, 1, rot),
                    block.TORCH[0], util.to_torch_dir_rot(util.TORCH_DIR_Z1, rot))
    elif torch_wall == 'z1':
        mc.setBlock(*util.to_rot(cx, cy, cz, halfside, halfside, side-2, rot),
                    block.TORCH[0], util.to_torch_dir_rot(util.TORCH_DIR_Z0, rot))
    else:
        mc.setBlock(*util.to_rot(cx, cy, cz, halfside, 1, halfside, rot),
                    block.STONE_BRICK_CHISELED)
        mc.setBlock(*util.to_rot(cx, cy, cz, halfside, 2, halfside, rot),
                    block.TORCH[0], util.TORCH_DIR_UP)
