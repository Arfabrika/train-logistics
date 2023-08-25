class Track:
    def __init__(self, track) -> None:
        self.fromst = track['from']
        self.tost = track['to']
        self.length = track['length']
        self.trackCnt = track['trackCnt'] if 'trackCnt' in track else 2
        self.direction = None if self.trackCnt == 1 else 'None'

    def swap(self):
         tmp = self.tost
         self.tost = self.fromst
         self.fromst = tmp

class Route:
    def __init__(self, route) -> None:
        self.id = route['id']
        self.tracks = []
        self.curTrack = route['curTrack'] if 'curTrack' in route else 0
        for track in route['tracks']:
            self.tracks.append(Track(track))
        self.distation = 0

    def checkPosition(self, position, speed):
        if self.tracks[self.curTrack].length - position <= speed:
            if self.isLastTrack():
                return 1
            return 0
        return -1

    def isLastTrack(self):
        if self.curTrack == len(self.tracks) - 1:
            return True
        return False

    def setDistation(self):
        self.distation = 0
        for track in self.tracks:
            self.distation += track.length

    def getTargetStation(self):
        return self.tracks[self.curTrack].tost

    def setRoute(self, start):
        if start == self.tracks[self.curTrack].fromst:
            return
        for i, track in enumerate(self.tracks):
            if track.fromst == start:
                self.curTrack = i
                self.linkTracks(start, self.tracks[-1].tost)
                return

        for i, track in enumerate(self.tracks):
            if track.tost == start:
                self.tracks[0:i+1] = self.tracks[0:i+1][::-1]
                self.linkTracks(start, self.tracks[-1].tost)

        if start == self.tracks[self.curTrack].tost:
            self.tracks[self.curTrack].swap()

    def setOneWayTrack(self, st):
        if self.tracks[self.curTrack].trackCnt == 1:
            self.tracks[self.curTrack].direction = st

    def linkTracks(self, start, stop):
        startInd = stopInd = -1
        for i, track in enumerate(self.tracks):
            if track.fromst == start:
                startInd = i
            if track.tost == stop:
                stopInd = i
        if startInd == stopInd:
            return
        for i in range(startInd, stopInd):
            if self.tracks[i].tost != self.tracks[i+1].fromst:
                self.tracks[i+1].swap()

    def checkTrack(self, dir, ind):
        if self.tracks[ind].trackCnt >= 2:
            return True
        if self.tracks[ind].direction is None or self.tracks[ind].direction == dir:
            return True
        return False

class DateRoute:
     def __init__(self, date, route) -> None:
          self.date = date
          self.route = route