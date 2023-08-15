import json
import pandas as pd
import psycopg2
from psycopg2 import Error
from transliterate import translit

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
        with open(fileName, 'r', encoding='utf-8') as f:
            return json.load(f)

    def saveToPostgres(self):
        try:
            connection = psycopg2.connect(user="postgres", password="123",
                                    host="127.0.0.1", port="5432",
                                    database="train-logistic")
        except (Exception, Error) as error:
            print("Ошибка при инициализации PostgreSQL", error)
        cursor = connection.cursor()
        for item in self.stationData.items():
            data = item[1]
            translitName = translit(item[0], language_code='ru', reversed=True)
            clear_table_query = f'''DROP TABLE IF EXISTS {translitName}'''
            cursor.execute(clear_table_query)
            connection.commit()
            if item[0] == 'Полярный':
                create_table_query = f'''CREATE TABLE IF NOT EXISTS {translitName}(id SERIAL PRIMARY KEY, date TIMESTAMP,oil_cnt INT,track1 VARCHAR(30),track1_unload VARCHAR(30), track2 VARCHAR(30),track2_unload VARCHAR(30), track3 VARCHAR(30),track3_unload VARCHAR(30));'''
                cursor.execute(create_table_query)
                connection.commit()
                for row in data:
                    if (len(row) < len(self.unloadStTitle)):
                        row.extend(['null'] * (len(self.unloadStTitle) - len(row)))
                    insert_query = f'''INSERT INTO {translitName}(date, oil_cnt, track1, track1_unload, track2, track2_unload, track3, track3_unload) VALUES('{row[0]}', {row[1]}, '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}');'''
                    cursor.execute(insert_query)
            else:
                create_table_query = f'''CREATE TABLE IF NOT EXISTS {translitName}(id SERIAL PRIMARY KEY, date TIMESTAMP, oil_cnt INT, oil_production INT, track1 VARCHAR(30),track1_unload INT);'''
                cursor.execute(create_table_query)
                connection.commit()
                for row in data:
                    if (len(row) < len(self.commStTitle)):
                        row.extend(['null'] * (len(self.commStTitle) - len(row)))
                    insert_query = f'''INSERT INTO {translitName}(date, oil_cnt, oil_production, track1, track1_unload) VALUES('{row[0]}', {row[1]}, {row[2]}, '{row[3]}', {row[4]});'''
                    cursor.execute(insert_query)
            connection.commit()
        cursor.close()
        connection.close()