import pytmx
import mineworld.util as util
import mineworld.room as room
import mineworld.corridor as corridor
import mineworld.map as map
import os
import glob
import mcpi.minecraft as minecraft
import mcpi.entity as entity
import argparse
import mcpi.block as block
import numpy as np
import math
import time

parser = argparse.ArgumentParser(description='Mineworld creator')
parser.add_argument('--roomdir', default="rooms",
                    help='Specify directory containing pickled rooms')
parser.add_argument('--server', default='localhost',
                    help='Minecraft running RaspberryJamMod')
parser.add_argument('--tiles', default='map1.tmx',
                    help='Tiled map using room files specified by --roomdir')
parser.add_argument('--l0', type=int, default=10,
                    help='Base level')
parser.add_argument('--hmax', type=int, default=10,
                    help='Height max (1/3rd of it downwards, 1/1 of it upwards)')
parser.add_argument('--map', default='cave_system.png',
                    help='Base map png')
parser.add_argument('--no-teleport', action="store_true",
                    help='Prevent rescuing and warping the player to start')
args = parser.parse_args()

rooms = {}
for rf in glob.glob("%s/*.pickle" % args.roomdir):
    r = room.load_room(rf)
    rooms[r.name] = r

mc = minecraft.Minecraft.create(address=args.server)

if not args.no_teleport:
    util.msg(mc, 'Rescuing player...')
    wh = mc.getHeight(0, 0)
    mc.setBlocks(-1, wh-1, -1, 1, wh-1, 1, block.GOLD_BLOCK)
    mc.player.setPos(0, wh, 0)

map.draw_map(mc, l0=args.l0, hmax=args.hmax, image=args.map)

tmxdata = pytmx.TiledMap(args.tiles)
for layer in tmxdata.visible_layers:
    if layer.name == 'dungeon':
        dungeon = layer
    if layer.name == 'mobs':
        mobs = layer

util.msg(mc, 'Drawing dungeon...')
for t in dungeon:
    if t.type != None:
        type = t.type
    else:
        type = os.path.splitext(os.path.basename(t.image[0]))[0]

    if type not in rooms and type not in ['tee', 'straight', 'intersection', 'corner', 'deadend']:
        print('Type %s not found in rooms %s' % (type, rooms.keys()))
        continue
    # TODO fix rotation to work regardless of number (e.g. -90)
    if t.rotation not in [-180, -90, 0, 90, 180, 270]:
        print('Type %s rotation %d not in right angles' % (type, t.rotation))
        continue

    # Force origin to the same spot, we are rotating around a centre
    x = int(t.x)
    z = int(t.y)
    if t.rotation == -180:
        t.rotation = 180
    if t.rotation == -90:
        t.rotation = 270
    if t.rotation == 90 or t.rotation == 180:
        z = z+util.TILE_SIZE
    if t.rotation == 180 or t.rotation == 270:
        x = x-util.TILE_SIZE

    print('Drawing "%s" at [%d,%d,%d]°%d' %
          (type, x, args.l0, z, t.rotation))

    if type in rooms:
        rooms[type].draw(mc, x, args.l0-2, z, rot=t.rotation)
    elif type == 'tee':
        corridor.draw_corridor(mc, x, args.l0-2, z, rot=t.rotation,
                               holes=[util.NORTH, util.WEST, util.SOUTH])
    elif type == 'straight':
        corridor.draw_corridor(mc, x, args.l0-2, z,
                               rot=t.rotation, holes=[util.NORTH, util.SOUTH])
    elif type == 'intersection':
        corridor.draw_corridor(mc, x, args.l0-2, z, rot=t.rotation,
                               holes=[util.NORTH, util.EAST, util.SOUTH, util.WEST])
    elif type == 'corner':
        corridor.draw_corridor(mc, x, args.l0-2, z,
                               rot=t.rotation, holes=[util.NORTH, util.WEST])
    elif type == 'deadend':
        corridor.draw_corridor(mc, x, args.l0-2, z,
                               rot=t.rotation, holes=[util.NORTH])
    else:
        print('* Unknown room or corridor')

start = None
entities = []
for t in mobs:
    if t.type != None:
        type = t.type
    else:
        type = os.path.splitext(os.path.basename(t.image[0]))[0]

    x = t.x
    y = args.l0
    z = t.y

    # Spawn on the floor, otherwise they don't spawn
    y = args.l0+1
    for scan_y in np.arange(args.l0, 0, -1):
        b = mc.getBlock(x, float(scan_y), z)
        if b != block.AIR[0]:
            break
        y = scan_y

    x = float(x)+0.5
    y = float(y)
    z = float(z)+0.5

    print('Loading "%s" at [%.1f,%.1f,%.1f]' % (type, x, y, z))
    mc.setBlocks(x, y, z, x, y+2, z, block.AIR)

    if type == 'start':
        start = (x, y, z)
    elif type == 'zombie':
        entities.append((entity.ZOMBIE, x, y, z))
    elif type == 'skeleton':
        entities.append((entity.SKELETON, x, y, z,
                        '{HandItems:[{id:beetroot,Count:1},{id:bone,Count:1}]}'))
    elif type == 'enderman':
        entities.append((entity.ENDERMAN, x, y, z))
    elif type == 'creeper':
        entities.append((entity.CREEPER, x, y, z))
    elif type == 'spider':
        entities.append((entity.SPIDER, x, y, z))
    elif type == 'minecart':
        entities.append((entity.MINECARTRIDEABLE, x, y-1, z))
    else:
        print('* Unknown entity')

# Begin!
if start != None and not args.no_teleport:
    mc.player.setPos(start)

util.msg(mc, 'READY!')


# If player is away from the chunk, the entities will not generate.
# Monitor the position and load entities as we go
while True:
    time.sleep(1)
    pos = mc.player.getPos()
    removals = []
    for ie in np.arange(0, len(entities), 1):
        e = entities[ie]
        if util.dist(pos.x, 0, pos.z, e[1], 0, e[3]) < 32.0:
            print('Spawning "%s" at [%.1f,%.1f,%.1f]' %
                  (e[0], e[1], e[2], e[3]))
            mc.spawnEntity(*e)
            removals.insert(0, ie)

    for r in removals:
        entities.pop(r)

    if pos.y > 200:
        mc.player.setPos(start)
