import pytmx
import mineworld.util as util
import mineworld.room as room
import mineworld.corridor as corridor
import os
import glob
import mcpi.minecraft as minecraft
import mcpi.entity as entity
import argparse

parser = argparse.ArgumentParser(description='Mineworld creator')
parser.add_argument('--roomdir', default="rooms",
                    help='Specify directory containing pickled rooms')
parser.add_argument('--server', default='localhost',
                    help='Minecraft running RaspberryJamMod')
parser.add_argument('--map', default='m.tmx',
                    help='Tiled map using room files specified by --roomdir')
args = parser.parse_args()

rooms = {}
for rf in glob.glob("%s/*.pickle" % args.roomdir):
    r = room.load_room(rf)
    rooms[r.name] = r

mc = minecraft.Minecraft.create(address=args.server)
mc.player.getPos()

tmxdata = pytmx.TiledMap(args.map)
for layer in tmxdata.visible_layers:
    if layer.name == 'dungeon':
        dungeon = layer
    if layer.name == 'mobs':
        mobs = layer

for t in dungeon:
    if t.type != None:
        type = t.type
    else:
        type = os.path.splitext(os.path.basename(t.image[0]))[0]

    if type not in rooms.keys() and type not in ['tee', 'straight', 'intersection', 'corner', 'deadend']:
        continue
    if t.rotation not in [0, 90, 180, 270]:
        continue

    # Force origin to the same spot, we are rotating around a centre
    x = int(t.x/util.TILE_SIZE)
    z = int(t.y/util.TILE_SIZE)
    if t.rotation == 90 or t.rotation == 180:
        z = z+1
    if t.rotation == 180 or t.rotation == 270:
        x = x-1

    print('Drawing "%s" at [%d,%d]°%d' % (type, x, z, t.rotation))

    if type in rooms:
        rooms[type].draw(mc, *util.to_world(x, 0, z), rot=t.rotation)
    elif type == 'tee':
        corridor.draw_corridor(mc, *util.to_world(x, 0, z), rot=t.rotation,
                               holes=[util.NORTH, util.WEST, util.SOUTH])
    elif type == 'straight':
        corridor.draw_corridor(mc, *util.to_world(x, 0, z),
                               rot=t.rotation, holes=[util.NORTH, util.SOUTH])
    elif type == 'intersection':
        corridor.draw_corridor(mc, *util.to_world(x, 0, z), rot=t.rotation,
                               holes=[util.NORTH, util.EAST, util.SOUTH, util.WEST])
    elif type == 'corner':
        corridor.draw_corridor(mc, *util.to_world(x, 0, z),
                               rot=t.rotation, holes=[util.NORTH, util.WEST])
    elif type == 'deadend':
        corridor.draw_corridor(mc, *util.to_world(x, 0, z),
                               rot=t.rotation, holes=[util.NORTH])
    else:
        print('* Unknown room or corridor')

for t in mobs:
    if t.type != None:
        type = t.type
    else:
        type = os.path.splitext(os.path.basename(t.image[0]))[0]

    x = int(t.x)
    z = int(t.y)

    print('Spawning "%s" at [%d,%d]' % (type, x, z))

    if type == 'zombie':
        mc.spawnEntity(entity.ZOMBIE, x, 1, z)
    elif type == 'skeleton':
        mc.spawnEntity(entity.SKELETON, x, 1, z,
                       '{HandItems:[{id:beetroot,Count:1},{id:bone,Count:1}]}')
    elif type == 'enderman':
        mc.spawnEntity(entity.ENDERMAN, x, 1, z)
    elif type == 'creeper':
        mc.spawnEntity(entity.CREEPER, x, 1, z)
    elif type == 'spider':
        mc.spawnEntity(entity.SPIDER, x, 1, z)
    else:
        print('* Unknown mob')
