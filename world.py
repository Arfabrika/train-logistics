import datetime
from station import Station
from unloadStation import UnloadStation
from train import Train
from dataworker import DataWorker
from route import Route
import copy

dw = DataWorker()

class World:
    def __init__(self) -> None:
        data = dw.loadJSON('inputData.json')

        # Time params
        self.curtime = datetime.datetime.strptime(data['curtime'], "%d-%m-%y %H:%M:%S")
        self.stoptime = datetime.datetime.strptime(data['stoptime'], "%d-%m-%y %H:%M:%S")

        # route params
        routesArr = []
        for route in data['routes']:
            routesArr.append(Route(route))

        # Train params
        # trains #0 - #2 R-P Small
        #        #3 - #4 R-P Big
        #        #5 - #6 Z-P
        self.trains = []
        exitTrainInd = None
        for i, tr in enumerate(data['trains']):
            curRoute = None
            if tr['name'] == "Выходной":
                exitTrainInd = i
            else:
                routeId = tr['routeId']
                for route in routesArr:
                    if route.id == routeId:
                        curRoute = copy.deepcopy(route)
                        break
                curRoute.setDistation()
            curTr = Train(tr, curRoute)
            self.trains.append(curTr)

        # Load station params
        self.stations = []
        for st in data['stations']:
            if 'unloadSpeed' in st:
                curSt = UnloadStation(st, self.trains[exitTrainInd])
            else:
                curSt = Station(st)
            self.stations.append(curSt)
        self.trains.pop(exitTrainInd)

        for tr in self.trains:
            if tr.route.tracks[0].fromst != tr.lastStation:
                tr.route.tracks[0].swap()
            if tr.position == 0:
                for st in self.stations:
                    if st.name == tr.route.tracks[0].fromst:
                        st.trains.append(tr)
                        break

    def worldStep(self):
        #print(self.curtime)
        for tr in self.trains:
            if tr.position >= tr.route.tracks[0].length:
                tr.arrive()
                stname = tr.route.getTargetStation()
                if tr.lastStation == stname:
                    ind = None
                    for i, st in enumerate(self.stations):
                        if st.name == stname:
                            ind = i
                            break
                    self.stations[ind].addTrain(tr)

        # station actions
        for st in self.stations:
            st.step()
            data = st.getData()
            data.insert(0, self.curtime.strftime('%d-%m-%y %H:%M:%S'))
            dw.saveOneRow(data[-1], data)
            print(data)

        # train steps
        self.moveTrains()

        for tr in self.trains:
            print(" ".join([tr.name, str(tr.curCap), str(tr.position), tr.lastStation]))
        self.curtime += datetime.timedelta(hours=1)

    def saveStats(self):
        dw.saveInExcel()

    def moveTrains(self):
        for tr in self.trains:
            flag = 1
            for st in self.stations:
                if tr in st.trains:
                  flag = 0
                  break
            if flag:
                tr.move()