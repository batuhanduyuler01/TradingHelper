import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from math import floor


class MACD :

    def __init__(self, dataframe, date = '2019-01-01', slow = 26, fast = 12, smooth = 9):
        # Initialize DataFrames
        #self.data = pd.read_csv("../past_work/Veri_Setleri/GARAN.IS.csv")
        self.data = dataframe.copy()
        self.data = self.data[self.data.Date > str(date)]
        self.data = self.data.set_index(pd.DatetimeIndex(self.data['Date'].values))
        self.macd_df = pd.DataFrame()
        # Initialize MACD calculator parameters
        self.slow = slow
        self.fast = fast 
        self.smooth = smooth
        # Initialize Strategy parameters
        self.__buy_price = list()
        self.__sell_price = list()
        self.macd_signal = list()
        self.signal = 0

    def getSellPriceInfo(self):
        return self.__sell_price
    def getBuyPriceInfo(self):
        return self.__buy_price

    def showData(self, isTrue):
        if (isTrue):
            print(self.data.head(10))
        else:
            print(self.macd_df.head(10))

    def getMACD(self):
        price = self.data.Close

        shortEMA = price.ewm(span = self.fast, adjust = False).mean()
        longEMA = price.ewm(span = self.slow, adjust = False).mean()
        MACD = pd.DataFrame(shortEMA - longEMA).rename(columns = {'Close': 'MACD'})
        signal = pd.DataFrame(MACD.ewm(span = self.smooth, adjust = False).mean()).rename(columns= {'MACD':'signal'})
        hist = pd.DataFrame(MACD["MACD"] - signal["signal"]).rename(columns = {0: 'hist'})

        frames = [MACD, signal, hist]
        self.macd_df = pd.concat(frames, join = 'inner', axis = 1)

    def implementStrategy(self):
        self.getMACD()

        prices = self.data.Close

        for element in range(len(self.macd_df)):

            if ((self.macd_df["MACD"][element]) > (self.macd_df["signal"][element])):
                if self.signal != 1:
                    self.__buy_price.append(prices[element])
                    self.__sell_price.append(np.nan)
                    self.signal = 1
                    self.macd_signal.append(self.signal)
                else:
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(np.nan)
                    self.macd_signal.append(0)
            elif ((self.macd_df["MACD"][element]) < (self.macd_df["signal"][element])):
                if self.signal != -1:
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(prices[element])
                    self.signal = -1
                    self.macd_signal.append(0)
                else:
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(np.nan)
                    self.macd_signal.append(0)
            else:
                self.__buy_price.append(np.nan)
                self.__sell_price.append(np.nan)
                self.macd_signal.append(0)

    def plotStrategy(self):
        self.implementStrategy()

        ax1 = plt.subplot2grid((15,1), (0,0), rowspan = 8, colspan = 1)
        ax2 = plt.subplot2grid((15,1), (10,0), rowspan = 8, colspan = 1)

        ax1.plot(self.data.Close , color = 'skyblue', linewidth = 2, label = 'KAĞIT')
        ax1.plot(self.data.index, self.__buy_price, marker = '^', color = 'green', markersize = 10, label = 'Alım Sinyali', linewidth = 0)     
        ax1.plot(self.data.index, self.__sell_price, marker = 'v', color = 'r', markersize = 10, label = 'Satış Sinyali', linewidth = 0)     
        ax1.legend()
        ax1.set_title('MACD Stratejisi')
        ax2.plot(self.macd_df['MACD'], color = 'grey', linewidth = 1.5, label = 'MACD')
        ax2.plot(self.macd_df['signal'], color = 'skyblue', linewidth = 1.5, label = 'Signal')

        for element in range(len(self.macd_df)):
            if str(self.macd_df['hist'][element])[0] == '-':
                ax2.bar(self.macd_df.index[element], self.macd_df['hist'][element], color = '#ef5350')
            else:
                ax2.bar(self.macd_df.index[element], self.macd_df['hist'][element], color = '#26a69a')
        plt.legend(loc = 'lower right')
        plt.show()



        

