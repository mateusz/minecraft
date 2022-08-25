import mcpi.block as block

NORTH = 'z0'
EAST = 'x1'
SOUTH = 'z1'
WEST = 'x0'

TORCH_DIR_X1 = 1
TORCH_DIR_X0 = 2
TORCH_DIR_Z1 = 3
TORCH_DIR_Z0 = 4
TORCH_DIR_UP = 5

TILE_SIZE = 9

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
    block.CARPET[0],
]

FACING = [
    block.TORCH[0],
    block.REDSTONE_TORCH_INACTIVE[0],
    block.REDSTONE_TORCH_ACTIVE[0],
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
