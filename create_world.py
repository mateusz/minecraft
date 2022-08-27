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

parser = argparse.ArgumentParser(description='Mineworld creator')
parser.add_argument('--roomdir', default="rooms",
                    help='Specify directory containing pickled rooms')
parser.add_argument('--server', default='localhost',
                    help='Minecraft running RaspberryJamMod')
parser.add_argument('--map', default='map1.tmx',
                    help='Tiled map using room files specified by --roomdir')
parser.add_argument('--l0', type=int, default=0,
                    help='Base level')
parser.add_argument('--no-start', action="store_true",
                    help='Prevent warping to start')
args = parser.parse_args()

rooms = {}
for rf in glob.glob("%s/*.pickle" % args.roomdir):
    r = room.load_room(rf)
    rooms[r.name] = r

mc = minecraft.Minecraft.create(address=args.server)

print('Rescuing player...')
wh = mc.getHeight(0, 0)
mc.setBlocks(-1, wh, -1, 1, wh, 1, block.GOLD_BLOCK)
mc.player.setPos(0, wh+2, 0)

map.draw_map(mc, 'cave_system.png')

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
    x = int(t.x)
    z = int(t.y)
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
for t in mobs:
    if t.type != None:
        type = t.type
    else:
        type = os.path.splitext(os.path.basename(t.image[0]))[0]

    x = int(t.x)+0.5
    y = args.l0-1
    z = int(t.y)+0.5

    print('Spawning "%s" at [%d,%d,%d]' % (type, x, args.l0, z))

    if type == 'start':
        start = (x, y, z)
    elif type == 'zombie':
        mc.spawnEntity(entity.ZOMBIE, x, y, z)
    elif type == 'skeleton':
        mc.spawnEntity(entity.SKELETON, x, y, z,
                       '{HandItems:[{id:beetroot,Count:1},{id:bone,Count:1}]}')
    elif type == 'enderman':
        mc.spawnEntity(entity.ENDERMAN, x, y, z)
    elif type == 'creeper':
        mc.spawnEntity(entity.CREEPER, x, y, z)
    elif type == 'spider':
        mc.spawnEntity(entity.SPIDER, x, y, z)
    else:
        print('* Unknown mob')

# Begin!
if start != None and not args.no_start:
    mc.player.setPos(start)
