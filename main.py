from world import World
world = World()

while world.curtime < world.stoptime:
    # print(world.curtime)
    world.worldStep()

    """
    class Train:
    def __init__(self, number, maxCap, curCap, 
                 speed, distation, 
                 position = 0, direction = 1,
                   isgone = 0) -> None:
        # position = 0 --> train in R station
        # direction = 1 --> R --> P
        #             0     R <-- P
        self.number = number
        self.maxCap = maxCap
        self.curCap = curCap
        self.speed = speed
        self.position = position
        self.direction = direction
        self.distation = distation
        self.isgone = isgone
        pass
    """