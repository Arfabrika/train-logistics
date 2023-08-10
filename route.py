
class Route:
    def __init__(self, id, stations, tracks, direction = 1) -> None:
        self.id = id
        self.stations = stations
        self.tracks = tracks
        self.distation = (self.sumTracks() if direction == 1 else 0)

    """
    1 - train arrive to final station (position = distantion)
    -1 - train arrive to start station (postion = 0)
    0 - train between stations 
    """
    def checkPosition(self, position, speed, direction):
        if self.distation - position <= speed and direction == 1:
            return 1
        if position - speed <= 0 and direction == -1:
            return -1
        return 0
    
    def sumTracks(self):
        sum = 0
        for track in self.tracks:
            sum += track
        return sum
    
    def setDistation(self, direction):
        if direction == 1:
            self.distation = self.sumTracks()
        else:
            self.distation = 0

    def getTargetStation(self, direction):
        if direction == 1:
            return self.stations[-1]
        return self.stations[0]