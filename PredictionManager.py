from datetime import date

from numpy.core.numeric import NaN
import MACD_class as macd
import RSI_class as rsi
import Database_class as db
import Bollinger_class as bb
import yFinance_class as yfHelper
import pandas as pd
import numpy as np


class PredictionManager:
    
    def __init__(self):
        self.DataBase = db.DataBase()
        self.DataBase.insertTable("../past_work/Veri_Setleri/GARANIS.csv", "garanti")

    def helpTrading(self, stockName, period, interval, printStrategy = False):
        self.yData = yfHelper.yFinance(stockName, period , interval)
        self.bollinger = bb.Bollinger(self.yData.getData(), date='2015-01-01')
        self.macd = macd.MACD(self.yData.getData(), date = '2015-01-01')
        self.rsi = rsi.RSI(self.yData.getData(), date = '2015-01-01')
        
        if (printStrategy):
            self.bollinger.plotStrategy()
            self.macd.plotStrategy()
            self.rsi.plotStrategy()
    def dropUnnecessaryColumns(self, dataframe):
        df = dataframe.copy()
        df = df.set_index(pd.DatetimeIndex(df['Date'].values))
        columnList = df.columns
        setupList = columnList[1:]
        for index, row in df.iterrows():
            flag = True
            for column in setupList:
                if type(row[column]) == type(3.8): 
                    flag = False
                else :
                    #print(type(row[column]))
                    pass
            
            if (flag):
                df.drop(index = index, inplace = True)

        print(df.head(50))
        return df


predictionManager = PredictionManager()
predictionManager.helpTrading('XU100.IS', '1y', '1d', False)

df = predictionManager.macd.saveStrategy()
df = predictionManager.rsi.saveStrategy(df)
df = predictionManager.bollinger.saveStrategy(df)
df = predictionManager.dropUnnecessaryColumns(df)
