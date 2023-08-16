from station import Station

class UnloadStation(Station):
    def __init__(self, st, exitTrain) -> None:
        self.name = st['name']
        self.loadSpeed = st['loadSpeed']
        self.unloadSpeed = st['unloadSpeed']
        self.curOilCount = st['curOilCount']
        self.maxOilCount = st['maxOilCount']
        self.exitTrain = exitTrain
        self.isRouteChanging = st['isRouteChanging']

        self.loadVals = [0] * 3
        self.stats = []
        self.trains = []

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
    
    def getUnloadValue(self, tr):
        if tr.curCap >= self.unloadSpeed:
            return self.unloadSpeed
        return tr.curCap

    def saveData(self, limit):
        for i, tr in enumerate(self.trains):
            if i == limit:
                break
            self.stats.append(tr.name)
            val = self.loadVals[i] if i < len(self.loadVals) else 0
            if val is None:
                self.stats.append('Ожидание')
            elif val > 0:
                self.stats.append('Погрузка: ' + str(val))
            elif val < 0:
                self.stats.append('Отгрузка: ' + str(-val))
            elif val == 0:
                self.stats.append('null')

        self.stats.append(self.name)

    def isExitTrainNeeded(self):
        for tr in self.trains:
            if tr.name == "Выходной":
                return False
        if self.curOilCount > 10000:
            return True
        return False

    def step(self, date):
        self.changeRoute(date)
        # train departure
        self.stats = [self.curOilCount]
        for tr in self.trains:
            ind = self.trains.index(tr)
            if tr.name == "Выходной" and tr.curCap == tr.maxCap:
                self.loadVals.pop(ind)
                tr.curCap = 0
                self.trains.remove(tr)
            elif tr.name != "Выходной" and tr.curCap == 0:
                self.loadVals.pop(ind)
                self.trains.remove(tr)

        # is oil train needed
        limit = min(3, len(self.trains))
        if limit > 3:
            for i in range(3, len(self.trains)):
                self.trains[i].waitingCnt += 1
        if self.isExitTrainNeeded():
            if limit < 3:
                self.trains.append(self.exitTrain)
            else:
                self.trains.insert(0, self.exitTrain)

        # train loading/unloading
        self.loadVals = [0] * limit
        for i in range(limit):
            curTrain = self.trains[i]
            if curTrain.name == "Выходной":
                self.loadVals[i] = -self.loadTrain(curTrain)
            else:
                if not self.isFull(self.getUnloadValue(tr)):
                    self.loadVals[i] = self.unloadOne(curTrain)
                else:
                    self.loadVals[i] = None
                    curTrain.waitingCnt += 1
        self.saveData(limit)

    def isFull(self, futureVal):
        sum = 0
        for val in self.loadVals:
            if val is not None and val > 0:
                sum += val
        if sum + self.curOilCount + futureVal >= self.maxOilCount:
            return True
        return False