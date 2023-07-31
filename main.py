from world import World

world = World()
while world.curtime < world.stoptime:
    print(world.curtime)
    world.incrTime()