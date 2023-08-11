import datetime
from station import Station, UnloadStation
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
            routesArr.append(Route(route['id'], route['stations'], route['tracks']))

        # Train params
        # trains #0 - #2 R-P Small
        #        #3 - #4 R-P Big
        #        #5 - #6 Z-P
        self.trains = []
        for tr in data['trains']:
            routeId = tr['routeId']
            curRoute = None
            for route in routesArr:
                if route.id == routeId:
                    curRoute = copy.deepcopy(route)
                    break
            curRoute.setDistation(tr['direction'] if 'direction' in tr else 1)
            curTr = Train(tr['name'], tr['maxCap'], curRoute,
                          tr['curCap'] if 'curCap' in tr else 0,
                          tr['speed'] if 'speed' in tr else 0,
                          tr['position'] if 'position' in tr else 0,
                          #tr['isgone'] if 'isgone' in tr else 0,
                          tr['direction'] if 'direction' in tr else 1)
            self.trains.append(curTr)

        # Load station params
        self.stations = []
        for st in data['stations']:
            if 'unloadSpeed' in st:
                exitTrain = Train(st['exitTrain']['name'], st['exitTrain']['maxCap'])
                curSt = UnloadStation(st['name'], st['loadSpeed'], 
                                      st['trains'] if 'trains' in st else [],
                                      st['unloadSpeed'], st['maxOilCount'], st['curOilCount'],
                                      exitTrain)
            else:
                curSt = Station(st['name'], st['loadSpeed'], 
                                st['trains'] if 'trains' in st else [],
                                st['curOilCount'], st['avgOil'], st['msdOil'])
            self.stations.append(curSt)

        for tr in self.trains:
            tr.checkStop()

    def worldStep(self):
        #print(self.curtime)

        for tr in self.trains:
            if tr.isgone:
                tr.isgone = 0
                stname = tr.route.getTargetStation(tr.direction)
                ind = None
                for i, st in enumerate(self.stations):
                    if st.name == stname:
                        ind = i
                        break
                tr.reverse()
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
            print(" ".join([tr.name, str(tr.curCap), str(tr.position)]))
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