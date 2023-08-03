import datetime
from station import Station, UnloadStation
from train import Train

class World:
    def __init__(self) -> None:
        
        # Time params
        self.curtime = datetime.datetime(2021,11,1)
        self.stoptime = datetime.datetime(2021,11,5)#datetime.datetime(2021,12,1)

        # Train params
        # trains #0 - #2 R-P Small
        #        #3 - #4 R-P Big
        #        #5 - #6 Z-P
        t0 = Train("Р-П М #1", 4000, 4000, 40, 2500, 1250, 1)
        t1 = Train("Р-П М #2", 4000, 0,    40, 2500, 0, 0, -1)
        t2 = Train("Р-П М #3", 4000, 4000, 400, 2500, 2500, 1, 1)
        t3 = Train("Р-П Б #1", 6000, 0,    35, 2500, 0, 1)
        t4 = Train("Р-П Б #2", 6000, 0,    35, 2500, 0, 1)
        testtrain = Train("Тест", 20, 0, 100, 0, 80, -1)
        #self.trains = [t0, t1, t2, t3, t4]#, testtrain]
        self.trains = [t2]
        # Load station params
        R = Station(200, [], 6000, 150, 10)
        #Z = Station(250, [], 5000, 50, 2)

        # Unload station params
        P = UnloadStation([])
        self.stations = [R, P]#, Z]
        pass

    def worldStep(self):
        print(self.curtime)
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

        #train steps
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