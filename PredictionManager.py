from datetime import date

from numpy.core.numeric import NaN
import MACD_class as macd
import RSI_class as rsi
import Database_class as db
import Bollinger_class as bb
import AlgorithmicTrading_class as algoManager
import yFinance_class as yfHelper
import pandas as pd
import numpy as np


class PredictionManager:
    
    def __init__(self, stockName, period, interval):
        """
        self.DataBase = db.DataBase()
        self.DataBase.insertTable("../past_work/Veri_Setleri/GARANIS.csv", "garanti")
        """
        self.algorithmHelper = algoManager.AlgorithmManager(stockName = stockName, period = period, interval = interval)

    def helpTrading(self):
        self.algorithmHelper.findOnlyTradings()
        self.algorithmHelper.printDataFrame(30)
        self.algorithmHelper.printOnlyTradings(30)
        self.algorithmHelper.getFinalDate()




predictionManager = PredictionManager('ETH-USD', '1y', '1d')
predictionManager.helpTrading()