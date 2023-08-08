
class Train:
    def __init__(self, name, maxCap, curCap = 0, speed = 0, distation = 0, 
                 position = 0, direction = 1, isgone = 0) -> None:
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
        self.direction = direction
        self.distation = distation
        self.isgone = isgone

# edit move function
    def move(self):
        if abs(self.distation - self.position) <= self.speed:#if self.position + self.speed * self.direction >= self.distation:
            self.position = self.distation
            self.isgone = 1
        else:
            self.position += self.speed * self.direction

    def reverse(self, newDist):
        self.isgone = 0
        self.direction *= -1
        self.distation = newDist