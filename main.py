from world import World
world = World()

dur = world.stoptime - world.curtime
dur_h = divmod(dur.total_seconds(), 3600)[0]
while world.curtime < world.stoptime:
        #  if world.curtime.strftime('%d-%m-%y %H:%M:%S') == '02-11-21 02:00:00':
        #     pass
         world.worldStep()
world.saveStats()

totalWaiting = 0
for tr in world.trains:
        totalWaiting += tr.waitingCnt
print("Absolute: " + str(totalWaiting))
print("%: " + str(totalWaiting / len(world.trains) / dur_h * 100))