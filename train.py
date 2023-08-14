from route import Route

class Train:
    def __init__(self, tr, route) -> None:
        # world schema
        # R           P           Z
        # |-----------|-----------|
        # 0          2500        6500  distation
        # direction = -1:  Z->P->R
        # direction = 1:  R->P->Z
        self.name = tr['name']
        self.maxCap = tr['maxCap']
        self.curCap = tr['curCap'] if 'curCap' in tr else 0
        self.speed = tr['speed'] if 'speed' in tr else 0
        self.position = tr['position'] if 'position' in tr else 0
        self.route = route
        self.lastStation = tr['lastStation'] if 'lastStation' in tr else None

        self.waitingCnt = 0

    def checkStop(self):
        res = self.route.checkPosition(self.position, self.speed)
        if res == 1:
            return True
        return False

    def move(self):
        if not self.checkStop():
            self.position += self.speed
        else:
            self.position = self.route.tracks[0].length

    def arrive(self):
        self.position = 0
        curTrack = None
        for track in self.route.tracks:
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