import datetime
from station import Station
from unloadStation import UnloadStation
from train import Train
from dataworker import DataWorker
from route import Route, DateRoute
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
            routesArr.append(copy.deepcopy(Route(route)))

        # Train params
        # trains #0 - #2 R-P Small
        #        #3 - #4 R-P Big
        #        #5 - #6 Z-P
        self.trains = []
        exitTrainInd = None
        for i, tr in enumerate(data['trains']):
            routeList = []
            if tr['name'] == "Выходной":
                exitTrainInd = i
            else:
                for routeDate in tr['routes']:
                    routeId = routeDate['routeId']
                    for route in routesArr:
                        if route.id == routeId:
                            curRoute = copy.deepcopy(route)
                            break
                    curRoute.setDistation()
                    routeList.append(copy.deepcopy(DateRoute(routeDate['startDate'], curRoute)))
            curTr = Train(tr, routeList)
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
            tr.routes[tr.curRoute].route.setRoute(tr.lastStation)
            tr.routes[tr.curRoute].route.setOneWayTrack(tr.lastStation)
            curTrack = tr.routes[tr.curRoute].route.curTrack
            self.updateOneWayStatus([{'status': tr.lastStation, 'routeId': tr.curRoute, 'trackId': curTrack}])
            if tr.position == 0:
                for st in self.stations:
                    if st.name == tr.routes[tr.curRoute].route.tracks[curTrack].fromst:
                        st.trains.append(tr)
                        break

    def worldStep(self):
        # print(self.curtime)
        for tr in self.trains:
            if (tr.position >= tr.routes[tr.curRoute].route.tracks[-1].length and 
                tr.routes[tr.curRoute].route.isLastTrack()):
                tr.position = 0
                tr.arrive()
                stname = tr.routes[tr.curRoute].route.getTargetStation()
                if tr.lastStation == stname:
                    ind = None
                    for i, st in enumerate(self.stations):
                        if st.name == stname:
                            ind = i
                            break
                    if ind is not None:
                        self.stations[ind].addTrain(tr)
                        curTrack = tr.routes[tr.curRoute].route.tracks[tr.routes[tr.curRoute].route.curTrack]
                        if curTrack.trackCnt == 1:
                            curTrack.direction = None
                            self.updateOneWayStatus([{'status': None, 'routeId': tr.curRoute, 'trackId': tr.routes[tr.curRoute].route.curTrack}])
                        tr.routes[tr.curRoute].route.curTrack = 0
                        tr.routes[tr.curRoute].route.tracks.reverse()
                        for track in tr.routes[tr.curRoute].route.tracks:
                            track.swap()

        # station actions
        for st in self.stations:
            st.step(self.curtime)
            data = st.getData()
            data.insert(0, self.curtime.strftime('%d-%m-%y %H:%M:%S'))
            dw.saveOneRow(data[-1], data)
            #print(data)

        # train steps
        self.moveTrains()

        # for tr in self.trains:
        #     print(" ".join([tr.name, str(tr.curCap), str(tr.position), tr.lastStation, str(tr.routes[tr.curRoute].route.curTrack)]))
        self.curtime += datetime.timedelta(hours=1)

    def saveStats(self):
        dw.saveInExcel()
        #dw.saveToPostgres()

    def moveTrains(self):
        for tr in self.trains:
            flag = 1
            for st in self.stations:
                if tr in st.trains:
                  flag = 0
                  break
            if flag:
                status = tr.move()
                if len(status) > 0:
                    self.updateOneWayStatus(status)

    def updateOneWayStatus(self, data):
        for elem in data:
            for tr in self.trains:
                if tr.routes[tr.curRoute].route.id == elem['routeId']:
                    tr.routes[tr.curRoute].route.tracks[elem['trackId']].direction = elem['status']