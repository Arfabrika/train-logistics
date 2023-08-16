import numpy as np
from train import Train

class Station:
    def __init__(self, st) -> None:
        self.name = st['name']
        self.loadSpeed = st['loadSpeed']
        
        self.curOilCount = st['curOilCount']
        self.avgOil = st['production']['avgOil']
        self.msdOil = st['production']['msdOil']
        self.isRouteChanging = st['isRouteChanging']

        self.curGeneratedOil = 0
        self.lastLoad = self.loadSpeed
        self.stats = []
        self.trains = []

    def generateOil(self):
        return int(np.random.normal(self.avgOil, self.msdOil, 1)[0])

    def step(self, date):
        self.changeRoute(date)
        self.curGeneratedOil = self.generateOil()
        if len(self.trains) > 1:
            for i in range(1, len(self.trains)):
                self.trains[i].waitingCnt += 1
        if (len(self.trains) > 0 and self.trains[0].maxCap == self.trains[0].curCap):
            self.trains.pop(0)

        self.saveData()
        self.curOilCount += self.curGeneratedOil
        if len(self.trains) != 0:
            self.loadTrain(self.trains[0])

    def saveData(self):
        self.stats = [self.curOilCount, 
                self.curGeneratedOil, 
                self.trains[0].name if len(self.trains) > 0 else "Null",
                self.lastLoad if len(self.trains) > 0 else "Null",
                self.name]

    def getData(self):
        return self.stats

    def addTrain(self, train):
        self.trains.append(train)

    def loadTrain(self, train):
        if self.curOilCount - self.loadSpeed > 0:
            if train.curCap + self.loadSpeed <= train.maxCap:
                train.curCap += self.loadSpeed
                self.curOilCount -= self.loadSpeed
                self.lastLoad = self.loadSpeed
            else:
                self.lastLoad = train.maxCap - train.curCap
                train.curCap += self.lastLoad
                self.curOilCount -= self.lastLoad
        else:
            if train.curCap + self.curOilCount <= train.maxCap:
                train.curCap += self.curOilCount
                self.lastLoad = self.curOilCount
                self.curOilCount = 0
            else:
                self.lastLoad = train.maxCap - train.curCap
                train.curCap += self.lastLoad
                self.curOilCount -= self.lastLoad
        return self.lastLoad

    def changeRoute(self, date):
        if self.isRouteChanging:
            for tr in self.trains:
                strtime = date.strftime('%d-%m-%y %H:%M:%S')
                for i, rd in enumerate(tr.routes):
                    if rd.date <= strtime and i != tr.curRoute and tr.curCap == 0:
                        tr.routes[tr.curRoute].date = '31-12-9999 23:59:59'
                        tr.curRoute = i
                        if tr.lastStation != tr.routes[tr.curRoute].route.tracks[0].fromst:
                            tr.routes[tr.curRoute].route.tracks[0].swap()
                        # print(f"{tr.name} changed route to {tr.curRoute} in {date.strftime('%d-%m-%y %H:%M:%S')}")