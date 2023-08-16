from route import Route

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

    def checkStop(self):
        if self.routes[self.curRoute].route.checkPosition(self.position, self.speed):
            return True
        return False

    def move(self):
        if not self.checkStop():
            self.position += self.speed
        else:
            self.position = self.routes[self.curRoute].route.tracks[0].length

    def arrive(self):
        self.position = 0
        curTrack = None
        for track in self.routes[self.curRoute].route.tracks:
            if track.fromst == self.lastStation:
                curTrack = track
                break
        self.lastStation = curTrack.tost
        track.swap()

    def findTrainInStations(self, stations):
        for st in stations:
            if self in st.trains:
                return True
        return False