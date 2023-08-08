import datetime
from station import Station, UnloadStation
from train import Train
from dataworker import DataWorker

dw = DataWorker()

class World:
    def __init__(self) -> None:
        data = dw.loadJSON('inputData.json')

        # Time params
        self.curtime = datetime.datetime.strptime(data['curtime'], "%d-%m-%y %H:%M:%S")
        self.stoptime = datetime.datetime.strptime(data['stoptime'], "%d-%m-%y %H:%M:%S")

        # Train params
        # trains #0 - #2 R-P Small
        #        #3 - #4 R-P Big
        #        #5 - #6 Z-P
        self.trains = []
        for tr in data['trains']:
            curTr = Train(tr['name'], tr['maxCap'],
                          tr['curCap'] if 'curCap' in tr else 0,
                          tr['speed'] if 'speed' in tr else 0,
                          tr['distation'] if 'distation' in tr else 0,
                          tr['position'] if 'position' in tr else 0,
                          tr['direction'] if 'direction' in tr else 0,
                          tr['isgone'] if 'isgone' in tr else 0)
            self.trains.append(curTr)

        # Load station params
        self.stations = []
        for st in data['stations']:
            if 'unloadSpeed' in st:
                exitTrain = Train(st['exitTrain']['name'], st['exitTrain']['maxCap'])
                curSt = UnloadStation(st['name'], st['loadSpeed'], st['trains'],
                                      st['unloadSpeed'], st['maxOilCount'], st['curOilCount'],
                                      exitTrain)
            else:
                curSt = Station(st['name'], st['loadSpeed'], st['trains'],
                                st['curOilCount'], st['avgOil'], st['msdOil'])
            self.stations.append(curSt)

    def worldStep(self):
        for tr in self.trains:
            if tr.isgone:
                if tr.distation == 0 and tr not in self.stations[0].trains:
                    tr.reverse(2500)
                    self.stations[0].addTrain(tr)

                #not tested
                elif tr.distation == 2500 and tr not in self.stations[1].trains:
                    if tr.direction == 1:
                        tr.reverse(0)
                    else:
                        tr.reverse(6500)
                    self.stations[1].addTrain(tr)
                elif tr.distation == 6500 and tr not in self.stations[2].trains:
                    tr.reverse(2500)
                    self.stations[2].addTrain(tr)

        # station actions
        for st in self.stations:
            st.step()
            data = st.getData()
            data.insert(0, self.curtime.strftime('%d-%m-%y %H:%M:%S'))
            dw.saveOneRow(data[-1], data)
            print(data)

        # train steps
        for tr in self.trains:
            flag = 1
            for st in self.stations:
                if tr in st.trains:
                  flag = 0
                  break
            if flag:
                tr.move()

        for tr in self.trains:
            print(" ".join([tr.name, str(tr.curCap), str(tr.position)]))
        self.curtime += datetime.timedelta(hours=1)

    def saveStats(self):
        dw.saveInExcel()