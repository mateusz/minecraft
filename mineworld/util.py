import mcpi.block as block
import time

NORTH = 'z0'
EAST = 'x1'
SOUTH = 'z1'
WEST = 'x0'

TORCH_DIR_X1 = 1
TORCH_DIR_X0 = 2
TORCH_DIR_Z1 = 3
TORCH_DIR_Z0 = 4
TORCH_DIR_UP = 5

STAIR_DIR_Z0 = 2
STAIR_DIR_Z1 = 3
STAIR_DIR_X1 = 1
STAIR_DIR_X0 = 0

STAIR_FLIP_DIR_Z0 = 6
STAIR_FLIP_DIR_Z1 = 7
STAIR_FLIP_DIR_X1 = 5
STAIR_FLIP_DIR_X0 = 4

SIGN_HUNG_Z1 = 2
SIGN_HUNG_Z0 = 3
SIGN_HUNG_X1 = 4
SIGN_HUNG_X0 = 5

TILE_SIZE = 9

MAP_STONE = (0, 0, 0, 255)

ATTACHABLES = [
    block.TORCH[0],
    block.REDSTONE_TORCH_INACTIVE[0],
    block.REDSTONE_TORCH_ACTIVE[0],
    block.DOOR_ACACIA[0],
    block.DOOR_BIRCH[0],
    # Fixed in the blocks.py to 197:
    block.DOOR_DARK_OAK[0],
    block.DOOR_IRON[0],
    block.DOOR_JUNGLE[0],
    block.DOOR_SPRUCE[0],
    block.DOOR_WOOD[0],
    (block.SIGN())[0],
    block.SIGN_HUNG[0],
    block.CARPET[0],
]

TORCHES = [
    block.TORCH[0],
    block.REDSTONE_TORCH_INACTIVE[0],
    block.REDSTONE_TORCH_ACTIVE[0],
]

STAIRS = [
    block.STAIRS_BIRCH[0],
    block.STAIRS_COBBLESTONE[0],
    block.STAIRS_JUNGLE[0],
    block.STAIRS_SPRUCE[0],
    block.STAIRS_WOOD[0],
    block.PURPUR_STAIRS[0],
    block.BRICK_STAIRS[0],
    block.STONE_BRICK_STAIRS[0],
    block.NETHER_BRICK_STAIRS[0],
    block.SANDSTONE_STAIRS[0],
    block.QUARTZ_STAIRS[0],
    block.ACACIA_STAIRS[0],
    block.DARK_OAK_STAIRS[0],
    block.RED_SANDSTONE_STAIRS[0],
]

# TODO implement rotation
ROT = [
    block.SKULL[0],
]


def to_tile(x, y, z):
    return [int(x/TILE_SIZE), int(y/TILE_SIZE), int(z/TILE_SIZE)]


def to_world(x, y, z):
    return [int(x*TILE_SIZE), int(y*TILE_SIZE), int(z*TILE_SIZE)]


def to_rot(sx, sy, sz, x, y, z, deg):
    if deg == 0:
        return [sx+x, sy+y, sz+z]
    if deg == 90:
        return [sx+TILE_SIZE-1-z, sy+y, sz+x]
    if deg == 180:
        return [sx+TILE_SIZE-1-x, sy+y, sz+TILE_SIZE-1-z]
    if deg == 270:
        return [sx+z, sy+y, sz+TILE_SIZE-1-x]


def to_torch_dir_rot(dir, deg):
    progression = {
        TORCH_DIR_X1: TORCH_DIR_Z1,
        TORCH_DIR_Z1: TORCH_DIR_X0,
        TORCH_DIR_X0: TORCH_DIR_Z0,
        TORCH_DIR_Z0: TORCH_DIR_X1,
    }
    if deg == 0:
        return dir
    if deg == 90:
        return progression[dir]
    if deg == 180:
        return progression[progression[dir]]
    if deg == 270:
        return progression[progression[progression[dir]]]


def to_stair_dir_rot(dir, deg):
    progression = {
        STAIR_DIR_X1: STAIR_DIR_Z1,
        STAIR_DIR_Z1: STAIR_DIR_X0,
        STAIR_DIR_X0: STAIR_DIR_Z0,
        STAIR_DIR_Z0: STAIR_DIR_X1,

        STAIR_FLIP_DIR_X1: STAIR_FLIP_DIR_Z1,
        STAIR_FLIP_DIR_Z1: STAIR_FLIP_DIR_X0,
        STAIR_FLIP_DIR_X0: STAIR_FLIP_DIR_Z0,
        STAIR_FLIP_DIR_Z0: STAIR_FLIP_DIR_X1,
    }
    if deg == 0:
        return dir
    if deg == 90:
        return progression[dir]
    if deg == 180:
        return progression[progression[dir]]
    if deg == 270:
        return progression[progression[progression[dir]]]


def to_sign_dir_rot(dir, deg):
    if deg == 0:
        return dir
    if deg == 90:
        return (dir + 4) % 16
    if deg == 180:
        return (dir + 8) % 16
    if deg == 270:
        return (dir + 12) % 16


def to_sign_hung_dir_rot(dir, deg):
    progression = {
        SIGN_HUNG_X1: SIGN_HUNG_Z1,
        SIGN_HUNG_Z1: SIGN_HUNG_X0,
        SIGN_HUNG_X0: SIGN_HUNG_Z0,
        SIGN_HUNG_Z0: SIGN_HUNG_X1,
    }
    if deg == 0:
        return dir
    if deg == 90:
        return progression[dir]
    if deg == 180:
        return progression[progression[dir]]
    if deg == 270:
        return progression[progression[progression[dir]]]
