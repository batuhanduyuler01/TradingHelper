from numpy.lib.function_base import append
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from math import floor

class Bollinger :
    def __init__(self, dataframe, date = '2019-01-01', window = 20):
        self.data = dataframe.copy()
        self.data = self.data[self.data.Date > str(date)]
        self.data = self.data.set_index(pd.DatetimeIndex(self.data['Date'].values))
        # Initialize SMA parameters
        self.window = window
        # Initialize Strategy parameters
        self.__buy_price = list()
        self.__sell_price = list()
        self.__BB_signal = list()
        self.__signal = 0
    def getBuyPriceInfo(self):
        return self.__buy_price
    def getSellPriceInfo(self):
        return self.__sell_price

    def __calculateSMA(self):
        self.__sma = self.data['Close'].rolling(window = self.window).mean()
        self.data[f'sma_{self.window}'] = self.__sma
        #print(self.data[f'sma_{self.window}'][:20])

    def obtainBB(self):
        self.__calculateSMA()

        std = self.data['Close'].rolling(window = self.window).std()
        self.__upper_bb = self.__sma + ( std * 2 )
        self.__lower_bb = self.__sma - ( std * 2 )

        self.data['upper_bb'] = self.__upper_bb
        self.data['lower_bb'] = self.__lower_bb
        #print(self.data.head(30))

    def implementStrategy(self):

        self.obtainBB()
        close = self.data.Close
        for i in range(len(close)):
            if ((close[i-1] > self.__lower_bb[i-1]) and (close[i] < self.__lower_bb[i])):
                if (self.__signal != 1):
                    self.__buy_price.append(close[i])
                    self.__sell_price.append(np.nan)
                    self.__signal = 1
                    self.__BB_signal.append(self.__signal)
                else:
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(np.nan)
                    self.__BB_signal.append(0)
            elif ((close[i-1] > self.__upper_bb[i-1]) and (close[i] < self.__upper_bb[i])):
                if (self.__signal != -1):
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(close[i])
                    self.__signal = -1
                    self.__BB_signal.append(self.__signal)
                else:
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(np.nan)
                    self.__BB_signal.append(0)
            else:
                self.__buy_price.append(np.nan)
                self.__sell_price.append(np.nan)
                self.__BB_signal.append(0)

    def plotStrategy(self):
        self.implementStrategy()

        self.data['Close'].plot(label = 'KAPANIŞ', alpha = 0.3)
        self.data['upper_bb'].plot(label = 'UPPER BB', linestyle = '--', linewidth = 1, color = 'black')
        self.data[f'sma_{self.window}'].plot(label = 'MIDDLE BB', linestyle = '--', linewidth = 1.2, color = 'grey')
        self.data['lower_bb'].plot(label = 'LOWER BB', linestyle = '--', linewidth = 1, color = 'black')
        plt.scatter(self.data.index, self.__buy_price, marker = '^', color = 'green', label = 'AL', s = 200)
        plt.scatter(self.data.index, self.__sell_price, marker = 'v', color = 'red', label = 'SAT', s = 200)
        plt.title(' Bollinger Band Stratejisi')
        plt.legend(loc = 'upper left')
        plt.show()


                









    
