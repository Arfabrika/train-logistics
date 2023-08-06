from world import World
world = World()

# try:
#     while world.curtime < world.stoptime:
#         world.worldStep()
# except Exception as e:
#     print(e)
#     world.saveStats()
while world.curtime < world.stoptime:
        world.worldStep()
world.saveStats()