import numpy as np
from train import Train

class Station:
    def __init__(self, name, loadSpeed, trains, curOilCount, avgOil, msdOil) -> None:
        self.name = name
        self.loadSpeed = loadSpeed
        self.trains = trains        
        self.curOilCount = curOilCount
        self.avgOil = avgOil
        self.msdOil = msdOil

        self.curGeneratedOil = 0
        self.lastLoad = loadSpeed
        self.stats = []

    def generateOil(self):
        return int(np.random.normal(self.avgOil, self.msdOil, 1)[0])

    def step(self):   
        self.curGeneratedOil = self.generateOil()
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
                self.loadSpeed = train.maxCap - train.curCap
                train.curCap += self.loadSpeed
                self.curOilCount -= self.loadSpeed
        else:
            train.curCap += self.curOilCount
            self.lastLoad = self.curOilCount
            self.curOilCount = 0
        return self.lastLoad

class UnloadStation(Station):
    def __init__(self, name, trains) -> None:   
        self.trains = trains
        self.name = name

        self.loadSpeed = 300
        self.unloadSpeed = 200
        self.curOilCount = 11000
        self.maxOilCount = 15000
        self.loadVals = [0] * 3
        self.exitTrain = Train("Выходной", 10000, 0, 0, 0)
        self.stats = []

    def unloadOne(self, tr):
        if tr.curCap >= self.unloadSpeed:
            tr.curCap -= self.unloadSpeed
            self.curOilCount += self.unloadSpeed
            return self.unloadSpeed
        else:
            self.curOilCount += tr.curCap
            tmp = tr.curCap
            tr.curCap = 0
            return tmp

    def saveData(self):
        self.stats = [self.curOilCount] 
        for i, tr in enumerate(self.trains):
            self.stats.append(tr.name)
            val = self.loadVals[i] if len(self.loadVals) else 0
            if val > 0:
                self.stats.append('Погрузка: ' + str(val))
            elif val < 0:
                self.stats.append('Отгрузка: ' + str(-val))
            else:
                self.stats.append('null')
        self.stats.append(self.name)

    def isExitTrainNeeded(self):
        for tr in self.trains:
            if tr.name == "Выходной":
                return False
        if self.curOilCount > 10000:
            return True
        return False

    def step(self):
        # train departure
        for tr in self.trains:
            ind = self.trains.index(tr)
            if tr.name == "Выходной" and tr.curCap == tr.maxCap:
                self.loadVals.pop(ind)
                self.trains.remove(tr)
            elif tr.curCap == 0:
                self.loadVals.pop(ind)
                self.trains.remove(tr)

        self.saveData()
        # is oil train needed
        if self.isExitTrainNeeded():
            self.trains.append(self.exitTrain)

        # train loading/unloading
        limit = min(3, len(self.trains))
        self.loadVals = [0] * limit
        for i in range(limit):
            curTrain = self.trains[i]
            if curTrain.name == "Выходной":
                self.loadVals[i] = -self.loadTrain(curTrain)
            else:
                self.loadVals[i] = self.unloadOne(curTrain)