from route import Route

class Train:
    def __init__(self, name, maxCap, route = Route(-1, [], []), curCap = 0, speed = 0, 
                 position = 0, direction = 1) -> None:
        # world schema
        # R           P           Z
        # |-----------|-----------|
        # 0          2500        6500  distation
        # direction = -1:  Z->P->R
        # direction = 1:  R->P->Z
        self.name = name
        self.maxCap = maxCap
        self.curCap = curCap
        self.speed = speed
        self.position = position
        self.isgone = 0 #isgone
        self.route = route
        self.direction = direction

    def checkStop(self):
        res = self.route.checkPosition(self.position, self.speed, self.direction)
        if res == 1:
            self.position = self.route.distation
            self.isgone = 1
            return True
        elif res == -1:
            self.position = 0
            self.isgone = 1
            return True
        return False

    def move(self):
        if not self.checkStop():
            self.position += self.speed * self.direction

    def reverse(self):
        #self.isgone = 0
        self.direction *= -1
        self.route.setDistation(self.direction)