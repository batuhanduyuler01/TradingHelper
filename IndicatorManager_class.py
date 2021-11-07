#This Class is made for implementation of the trading algorithm
from datetime import date
from numpy.core.numeric import NaN
import MACD_class as macd
import RSI_class as rsi
import Database_class as db
import Bollinger_class as bb
import yFinance_class as yfHelper
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class IndicatorManager():
    def __init__(self, stockName, period, interval):
        self.yData = yfHelper.yFinance(stockName, period, interval)
        self.bollinger = bb.Bollinger(self.yData.getData(), date='2015-01-01')
        self.macd = macd.MACD(self.yData.getData(), date='2015-01-01')
        self.rsi = rsi.RSI(self.yData.getData(), date='2015-01-01')
        self.__commonDataframe = pd.DataFrame()
        self.__onlyTradingDataFrame = pd.DataFrame()
        self.__printableDataFrame = pd.DataFrame()
        self.__isReady = 0 #it informs you about strategy is prepared or not

    def prepareStrategies(self):
        self.macd.implementStrategy()
        self.rsi.implementStrategy()
        self.bollinger.implementStrategy()
        
        self.__commonDataframe["Date"] = (self.yData.getData())['Date']
        self.__commonDataframe["Macd_Buy_Position"] = self.macd.getBuyPriceInfo()
        self.__commonDataframe["Macd_Sell_Position"] = self.macd.getSellPriceInfo()
        self.__commonDataframe["RSI_Buy_Position"] = self.rsi.getBuyPriceInfo()
        self.__commonDataframe["RSI_Sell_Position"] = self.rsi.getSellPriceInfo()
        self.__commonDataframe["Bollinger_Buy_Position"] = self.bollinger.getBuyPriceInfo()
        self.__commonDataframe["Bollinger_Sell_Position"] = self.bollinger.getSellPriceInfo()

    def adjustClosingPrice(self):
        self.__closePrices = self.yData.getData()
        self.__closePrices = self.__closePrices[["Date", "Close"]]
        self.__closePrices = self.__closePrices.set_index(pd.DatetimeIndex(self.__closePrices['Date'].values))
        self.__closePrices = self.__closePrices.drop(["Date"], axis = 1)

    def plotStrategy(self):
        #Geçici fonksiyon. İlerde qt veya django ile butonlu strateji bastırma yapısına geçilmeli
        #TODO: bu plot kısmı ilerletilebilir ve PredictionManager'a taşınabilir.
        self.strategyName = input("Enter one of them: \n1-Bollinger\n2-MACD\n3-RSI")
        if (self.strategyName.lower() == "bollinger"):
            self.bollinger.plotStrategy()
        elif (self.strategyName.lower() == "macd"):
            self.macd.plotStrategy()
        elif (self.strategyName.lower() == "rsi"):
            self.rsi.plotStrategy()
        else:
            self.bollinger.plotStrategy()
            self.macd.plotStrategy()
            self.rsi.plotStrategy()

    def findOnlyTradings(self):
        if (self.__isReady):
            pass
        else:
            self.prepareStrategies()
            self.__isReady = 1

        df = self.getCommonDataframe().copy()
        df = df.set_index(pd.DatetimeIndex(df['Date'].values))
        columnList = df.columns
        setupList = columnList[1:]
        for index, row in df.iterrows():
            flag = True
            for column in setupList:
                if type(row[column]) == type(3.8):
                    flag = False
                else:
                    pass

            if (flag):
                df.drop(index=index, inplace=True)
        self.adjustClosingPrice()
        merged_df = df.merge(self.__closePrices, left_index=True, right_index=True)
        self.__onlyTradingDataFrame = merged_df.copy()
        return df

    def preparePrintableDataframe(self):
        if (self.__isReady):
            pass
        else:
            self.prepareStrategies()
            self.__isReady = 1
    
        self.adjustClosingPrice()
        self.__printableDataFrame = self.__commonDataframe.copy()
        self.__printableDataFrame = self.__printableDataFrame.set_index(pd.DatetimeIndex(self.__printableDataFrame["Date"].values))
        self.__printableDataFrame = self.__printableDataFrame.merge(self.__closePrices, left_index=True, right_index=True)

    def printCommonDataFramewithClose(self, rowNumber = 50):
        self.preparePrintableDataframe()
        print(self.__printableDataFrame.tail(rowNumber))

    def printDataFrame(self , rowNumber = 50):
        print(self.__commonDataframe.tail(rowNumber))

    def printOnlyTradings(self, rowNumber = 30):
        self.findOnlyTradings()
        print(self.__onlyTradingDataFrame.tail(rowNumber))

    def getCommonDataframe(self):
        return self.__commonDataframe

    def getTradingDf(self):
        self.findOnlyTradings()
        return self.__onlyTradingDataFrame

    def getPrintableDf(self):
        self.preparePrintableDataframe()
        return self.__printableDataFrame


        


