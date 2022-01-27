import sys
sys.path.insert(0, '../../current_work/helpers')
sys.path.insert(0, '../../current_work/indicators')
sys.path.insert(0, '../../current_work/deeplearning')
import numpy as np
import pandas as pd
import managers.PredictionManager as pm
import helpers.backtest_class as backtestManager

class AlgoManager():
    def __init__(self):
        print("Algorithm Manager has invoke.")

    def initializeAlgoManager(self, stockChoice, predictionPeriod, predictionInterval) :
        self.myPredictions = pm.PredictionManager(stockChoice, predictionPeriod, predictionInterval)
        self.genelVeri = self.myPredictions.indicatorManager.get_strategy_df_all()

    def startProcess(self):
        #TODO: batuhan.duyuler: Burası for dönecek. Tek tek veri seti ismi ayıklamaktansa 
        #TODO: batuhan.duyuler: Date baş, Close son ve i. kolon şeklinde backteste sokulacak.
        rsi_df = self.genelVeri[["Date", "RSI", "Close"]]
        macd_df = self.genelVeri[["Date", "MACD", "Close"]]
        rsi_safe_df = self.genelVeri[["Date", "RSI_Safe", "Close"]]
        bollinger_df = self.genelVeri[["Date", "BollingBand", "Close"]]

        self.karList = []
        myBackTest = backtestManager.BackTesting(rsi_safe_df)
        myBackTest.implementBackTestNew()
        self.karList.append(["RSI Safe Sell", myBackTest.yuzdelikDurum])

        myBackTest = backtestManager.BackTesting(macd_df)
        myBackTest.implementBackTestNew()
        self.karList.append(["MACD", myBackTest.yuzdelikDurum])

        myBackTest = backtestManager.BackTesting(rsi_df)
        myBackTest.implementBackTestNew()
        self.karList.append(["RSI Düz (30-70)", myBackTest.yuzdelikDurum])

        myBackTest = backtestManager.BackTesting(bollinger_df)
        myBackTest.implementBackTestNew()
        self.karList.append(["Bolling Band ", myBackTest.yuzdelikDurum])

        self.karList = sorted(self.karList, key = lambda x : x[1])
        print(f"En Başarılı Algoritma: {self.karList[-1][0]}")
        print(f"yuzdelik durum: %{self.karList[-1][1] * 100}")

    def getBestStrategy(self):
        bestStrategy = self.karList[-1][0]
        bestProfit = self.karList[-1][1] * 100
        return bestStrategy, bestProfit
       

        
        



