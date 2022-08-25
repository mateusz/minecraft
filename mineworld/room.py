import pickle
import numpy as np
from . import util
from PIL import Image
import random
import mcpi.minecraft as minecraft
import mcpi.block as block


def load_room(path):
    with open(path, 'rb') as f:
        spec = pickle.load(f)
        return Room(
            name=spec['name'],
            side=spec['side'],
            door_style=spec['door_style'],
            source_location=spec['source_location'],
            version=spec['version'],
            blocks=spec['blocks'],
        )


class Room:
    def __init__(self, name, side, door_style, source_location, version, blocks):
        self.name = name
        self.side = side
        self.door_style = door_style
        self.source_location = source_location
        self.version = version
        self.blocks = blocks

    def draw(self, mc, px, py, pz, rot=0):
        px = float(px)
        py = float(py)
        pz = float(pz)

        i = 0
        for y in np.arange(0, self.side, 1):
            for x in np.arange(0, self.side, 1):
                for z in np.arange(0, self.side, 1):
                    b = self.blocks[i]
                    if b[0] not in util.ATTACHABLES:
                        mc.setBlockWithNBT(
                            *util.to_rot(px, py, pz, x, y, z, rot), b)
                    i += 1

        i = 0
        for y in np.arange(0, self.side, 1):
            for x in np.arange(0, self.side, 1):
                for z in np.arange(0, self.side, 1):
                    b = self.blocks[i]
                    if b[0] in util.FACING:
                        br = block.Block(
                            b[0], util.to_torch_dir_rot(b[1], rot), b[2])
                        mc.setBlockWithNBT(
                            *util.to_rot(px, py, pz, x, y, z, rot), br)
                    elif b[0] in util.ATTACHABLES:
                        mc.setBlockWithNBT(
                            *util.to_rot(px, py, pz, x, y, z, rot), b)
                    i += 1

    def get_block_at(self, x, y, z):
        return self.blocks[y*self.side*self.side+x*self.side+z]

    def door_dir(self):
        # X1 = tile image down
        # X0 = tile image up
        # Z1 = tile image right
        # Z0 = tile image left
        conversion = {
            'down': 'x1',
            'up': 'x0',
            'right': 'z1',
            'left': 'z0',
        }

        return conversion[self.door_style]

    def get_image_at_y(self, y=1):
        pixels = []
        for z in np.arange(0, self.side, 1):
            for x in np.arange(0, self.side, 1):
                #px = self.get_block_at(*to_rot(0,0,0,x,y,z,180)).getRGBA()
                px = self.get_block_at(x, y, z).getRGBA()
                pixels.append([px[0], px[1], px[2]])

        pixels = np.array(pixels, dtype=np.uint8).reshape((9, 9, 3))
        return Image.fromarray(pixels)

    def write(self, dir='rooms'):
        with open('%s/%s.pickle' % (dir, self.name), 'wb') as f:
            pickle.dump({
                'name': self.name,
                'side': self.side,
                'door_style': self.door_style,
                'source_location': self.source_location,
                'version': self.version,
                'blocks': self.blocks,
            }, f)
