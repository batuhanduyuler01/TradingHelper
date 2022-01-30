from functools import singledispatch
from numpy.lib.function_base import append
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.series import Series
from sklearn.covariance import ledoit_wolf_shrinkage 

class Stochastic :
    def __init__(self, dataframe, date = "01.01.2019", lookback = 14):
        self.data = dataframe.copy()
        self.data = self.data[self.data.Date > str(date)]
        self.data = self.data.set_index(pd.DatetimeIndex(self.data['Date'].values))
        self.Stochastic_df = pd.DataFrame()
        self.upper_band = 80
        self.lower_band = 20
        self.__buy_price = []
        self.__sell_price = []
        self.Stochastic_signal = []
        self.signal = 0
        self.prices = self.data.Close
        self.lookback = lookback

    def GetSellPriceInfo(self):
        return self.__sell_price

    def GetBuyPriceInfo(self):
        return self.__buy_price

    def CalculateStochastic(self):
        
        stochasticlist = []

        for i in range(1,len(self.prices)):

            if i == 1:
                cost = self.prices[-i]
                Lower14 = min(self.prices[-i-14:])
                High14 = max(self.prices[-i-14:])
                K = ((cost-Lower14)/[High14-Lower14])*100
                stochasticlist.append(K)

            else :
                cost = self.prices[-i]
                Lower14 = min(self.prices[-i-14:-i+1])
                High14 = max(self.prices[-i-14:-i+1])
                K = ((cost-Lower14)/[High14-Lower14])*100
                stochasticlist.append(K)
        return stochasticlist


    """def CalculatesSlowStochastic(self.prices):
        
        sumK = 0
        smalist = CalculateStochastic(self.prices)
        for i in (smalist):
            sumK = sumK + i
        itemlen = len(smalist)
        SMAK = sumK/itemlen
    """

    def implementStrategy(self):
        checkstochastic = self.CalculateStochastic()
        

        for element in range(1,len(checkstochastic)):
            if ((checkstochastic[element - 1] > self.lower_band) and (checkstochastic[element] < self.lower_band)):
                if (self.signal != 1):
                    self.__buy_price.append(self.prices[element])
                    self.__sell_price.append(np.nan)
                    self.signal = 1
                    self.Stochastic_signal.append(self.signal)
                else:
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(np.nan)
                    self.Stochastic_signal.append(0)

            elif ((checkstochastic[element - 1] < self.upper_band) and (checkstochastic[element] > self.upper_band)):
                if (self.signal != -1):
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(self.prices[element])
                    self.signal = -1
                    self.Stochastic_signal.append(self.signal)
                else:
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(np.nan)
                    self.Stochastic_signal.append(0)
            else:
                self.__buy_price.append(np.nan)
                self.__sell_price.append(np.nan)
                self.Stochastic_signal.append(0)

    def plotStrategy(self):

        self.implementStrategy()

        ax1 = plt.subplot2grid((15,1), (0,0), rowspan = 8, colspan = 1)
        ax2 = plt.subplot2grid((15,1), (10,0), rowspan = 8, colspan = 1)
        
        ax1.plot(self.data.Close, linewidth = 2.5, color = 'skyblue', label = 'Kağıt')
        ax1.plot(self.data.index, self.__buy_price, marker = '^', markersize = 10, color = 'green', label = 'AL')
        ax1.plot(self.data.index, self.__sell_price, marker = 'v', markersize = 10, color = 'r', label = 'SAT')
        ax1.set_title('Stochastic Indikatörü')
        ax2.plot(self.data['Stochastic_14'], color = 'orange', linewidth = 2.5)
        ax2.axhline(30, linestyle = '--', linewidth = 1.5, color = 'grey')
        ax2.axhline(70, linestyle = '--', linewidth = 1.5, color = 'grey')
        plt.show()
    
    def showData(self):
        self.CalculateStochastic()
        print("--------")
        print(self.data.head(10))

    def getStrategyDF(self):
        temp_df = pd.DataFrame(list(zip(self.data.Date[1:].to_list(), self.data.Close[1:].to_list(), self.Stochatic_signal)), columns=["Date", "Close", "Signal"])
        return temp_df


