from world import World
world = World()

# try:
#     while world.curtime < world.stoptime:
#         world.worldStep()
# except Exception as e:
#     print(e)
#     world.saveStats()
while world.curtime < world.stoptime:
        #  if world.curtime.strftime('%d-%m-%y %H:%M:%S') == '02-11-21 02:00:00':
        #     pass
         world.worldStep()
world.saveStats()