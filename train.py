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
        status = []
        res = self.routes[self.curRoute].route.checkPosition(self.position, self.speed)
        if res == -1:
            self.position += self.speed
        else:
            length = self.routes[self.curRoute].route.tracks[self.routes[self.curRoute].route.curTrack].length
            if res == 1:
                newPos = length
            else:
                newPos = self.speed - (length - self.position)
            curTrack = self.routes[self.curRoute].route.curTrack
            
            if curTrack + 1 < len(self.routes[self.curRoute].route.tracks):
                if self.routes[self.curRoute].route.checkTrack(self.routes[self.curRoute].route.tracks[curTrack].tost, curTrack + 1):
                    self.routes[self.curRoute].route.curTrack += 1
                    self.routes[self.curRoute].route.tracks[curTrack].direction = None
                    self.routes[self.curRoute].route.tracks[curTrack + 1].direction = self.routes[self.curRoute].route.tracks[curTrack].fromst
                    if self.routes[self.curRoute].route.tracks[curTrack].trackCnt == 1:
                        status.append({'status': None, 'routeId': self.curRoute, 'trackId': curTrack})
                    if self.routes[self.curRoute].route.tracks[curTrack + 1].trackCnt == 1:
                        status.append({'status': self.routes[self.curRoute].route.tracks[curTrack].fromst, 'routeId': self.curRoute, 'trackId': curTrack + 1})
                    self.arrive()
                else:
                    newPos = length
            self.position = newPos
        return status

    def arrive(self):
        curTrack = None
        for track in self.routes[self.curRoute].route.tracks:
            if track.fromst == self.lastStation:
                curTrack = track
                break
        self.lastStation = curTrack.tost