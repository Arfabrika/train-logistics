import pandas as pd

class DataWorker:

    def __init__(self) -> None:
        self.commStTitle = ['Дата события', 'Остаток нефти', 'Добыча', 'Состав на пути 1', 'Отгрузка на пути 1']
        self.unloadStTitle = ['Дата события', 'Остаток нефти', 'Состав на пути 1', 'Действие на пути 1',
                              'Состав на пути 2', 'Действие на пути 2', 'Состав на пути 3', 'Действие на пути 3' ]
        self.stationData = {}

    def saveOneRow(self, sheetName, data):
        if self.stationData.get(sheetName, -1) == -1:
            self.stationData[sheetName] = [data[0:-1]]
        else:
            self.stationData[sheetName].append(data[0:-1])

    def saveInExcel(self):
        writer = pd.ExcelWriter('train.xlsx', engine='xlsxwriter')
        for item in self.stationData.items():
            data = item[1]
            if item[0] == 'Полярный':
                for row in data:
                    if (len(row) < len(self.unloadStTitle)):
                        row.extend(['null'] * (len(self.unloadStTitle) - len(row)))
                df = pd.DataFrame(data, columns = self.unloadStTitle)
            else:
                df = pd.DataFrame(data, columns = self.commStTitle)
            df.to_excel(writer, sheet_name=item[0])
        writer.close()

    def loadJSON(self, fileName):
        pass