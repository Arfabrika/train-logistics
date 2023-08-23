class Train:
    def __init__(self, tr, routes) -> None:
        self.name = tr['name']
        self.maxCap = tr['maxCap']
        self.curCap = tr['curCap'] if 'curCap' in tr else 0
        self.speed = tr['speed'] if 'speed' in tr else 0
        self.position = tr['position'] if 'position' in tr else 0
        self.routes = routes
        self.lastStation = tr['lastStation'] if 'lastStation' in tr else None

        self.waitingCnt = 0
        self.curRoute = 0

    def move(self):
        res = self.routes[self.curRoute].route.checkPosition(self.position, self.speed)
        if res == -1:
            self.position += self.speed
        else:
            length = self.routes[self.curRoute].route.tracks[self.routes[self.curRoute].route.curTrack].length
            if res == 1:
                newPos = length
            else:
                newPos = self.speed - (length - self.position)
            if self.routes[self.curRoute].route.curTrack + 1 < len(self.routes[self.curRoute].route.tracks):
                self.routes[self.curRoute].route.curTrack += 1
                self.arrive()
            self.position = newPos

    def arrive(self):
        curTrack = None
        for track in self.routes[self.curRoute].route.tracks:
            if track.fromst == self.lastStation:
                curTrack = track
                break
        self.lastStation = curTrack.tost