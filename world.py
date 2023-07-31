import datetime

class World:
    def __init__(self) -> None:
        self.curtime = datetime.datetime(2021,11,1)
        self.stoptime = datetime.datetime(2021,12,1)
        pass

    def incrTime(self):
        self.curtime += datetime.timedelta(hours=1)