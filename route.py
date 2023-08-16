class Track:
    def __init__(self, track) -> None:
        self.fromst = track['from']
        self.tost = track['to']
        self.length = track['length']

    def swap(self):
         tmp = self.tost
         self.tost = self.fromst
         self.fromst = tmp

class Route:
    def __init__(self, route) -> None:
        self.id = route['id']
        self.tracks = []
        for track in route['tracks']:
            self.tracks.append(Track(track))
        self.distation = 0

    def checkPosition(self, position, speed):
        if self.distation - position <= speed:
            return 1
        return 0

    def setDistation(self):
        self.distation = 0
        for track in self.tracks:
            self.distation += track.length

    def getTargetStation(self):
            return self.tracks[0].fromst

class DateRoute:
     def __init__(self, date, route) -> None:
          self.date = date
          self.route = route