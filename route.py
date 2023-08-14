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

    """
    1 - train arrive to final station (position = distantion)
    -1 - train arrive to start station (postion = 0)
    0 - train between stations 
    """
    def checkPosition(self, position, speed):
        if self.distation - position <= speed:
            return 1
        return 0
    
    def sumTracks(self):
        sum = 0
        for track in self.tracks:
            sum += track.length
        return sum
    
    def setDistation(self):
            self.distation = self.sumTracks()

    def getTargetStation(self):
            return self.tracks[0].fromst