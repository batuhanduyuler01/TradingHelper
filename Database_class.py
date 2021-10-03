import sqlite3
from numpy.lib.function_base import insert
import pandas as pd

class DataBase :
    def __init__(self):
        self.db = sqlite3.connect('kagitlar.sqlite')
        self.im = self.db.cursor()
        self.df = pd.DataFrame()
        print("DB Connected!")

    def __del__(self):
        self.db.close()
        del self.df
        print("DB Connection Closed!")
    
    def printCSV(self, table_name):
        self.df = pd.read_sql_query(f"SELECT * from {table_name}", self.db)
        print(self.df.head(10))

    def updateTable(self, path, table_name ):
        self.df = pd.read_csv(str(path))
        self.temp_df = pd.read_sql_query(f"SELECT * from {table_name}", self.db)
        self.last_date = self.temp_df.iloc[-1,0]
        self.df = self.df[self.df.Date > str(self.last_date)]
        self.df.to_sql(str(table_name), self.db, if_exists="append", index = False)

    def insertTable(self, path, table_name):
        self.df = pd.read_csv(str(path))
        self.df.to_sql(str(table_name), self.db, if_exists='replace', index = False)

    def getTable(self):
        return self.df

