from functools import singledispatch
from numpy.lib.function_base import append
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.series import Series 

class RSI:
    def __init__(self, dataframe, date = '2019-01-01', lookback = 7):
        # Initialize Dataframe Parameters
        #self.data = pd.read_csv("../past_work/Veri_Setleri/GARAN.IS.csv")
        self.data = dataframe.copy()
        self.data = self.data[self.data.Date > str(date)]
        self.data = self.data.set_index(pd.DatetimeIndex(self.data['Date'].values))
        self.df_RSI = pd.DataFrame()
        self.lower_band = 15
        self.upper_band = 85

        # Initialize Strategy Parameters
        self.__buy_price = []
        self.__sell_price = []
        self.rsi_signal = []
        self.signal = 0
        self.prices = self.data.Close
        self.lookback = lookback
    def getSellPriceInfo(self):
        return self.__sell_price
    def getBuyPriceInfo(self):
        return self.__buy_price

    def __obtainRSI(self):
        close = self.data.Close #self.prices ile değiştirilebilir ileride
        ret = close.diff()
        up = []
        down = []

        for element in range(len(ret)):
            if (ret[element] < 0):
                up.append(0)
                down.append(ret[element])
            elif (ret[element] >= 0):
                up.append(ret[element])
                down.append(0)
    
        upSeries = pd.Series(up)
        downSeries = pd.Series(down).abs()

        upEwm = upSeries.ewm(com = self.lookback - 1, adjust = False).mean()
        downEwm = downSeries.ewm(com = self.lookback - 1, adjust = False).mean()
        rs = upEwm / downEwm
        rsi = 100 - (100 / (1 + rs))
            #diff aldığımız için ilk elemana karşılık gelen ret boşta kalıyor
            #RSI hesaplarında n gün varsa (n-1) RSI değeri elde etmiş oluyoruz
            #bu nedenle ilk indeksi dropluyoruz
        close = close.drop(index = close.index[0])
        temp_df = pd.DataFrame(rsi).rename(columns={0 : 'rsi'}).set_index(close.index)
        self.data['RSI_14'] = temp_df[3:]

    def implementStrategy(self):
        self.__obtainRSI()
        rsi = self.data.RSI_14

        for element in range(0,len(rsi)):
            if ((rsi[element - 1] > self.lower_band) and (rsi[element] < self.lower_band)):
                if (self.signal != 1):
                    self.__buy_price.append(self.prices[element])
                    self.__sell_price.append(np.nan)
                    self.signal = 1
                    self.rsi_signal.append(self.signal)
                else:
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(np.nan)
                    self.rsi_signal.append(0)

            elif ((rsi[element - 1] < self.upper_band) and (rsi[element] > self.upper_band)):
                if (self.signal != -1):
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(self.prices[element])
                    self.signal = -1
                    self.rsi_signal.append(self.signal)
                else:
                    self.__buy_price.append(np.nan)
                    self.__sell_price.append(np.nan)
                    self.rsi_signal.append(0)
            else:
                self.__buy_price.append(np.nan)
                self.__sell_price.append(np.nan)
                self.rsi_signal.append(0)
    
    def plotStrategy(self):

        self.implementStrategy()

        ax1 = plt.subplot2grid((15,1), (0,0), rowspan = 8, colspan = 1)
        ax2 = plt.subplot2grid((15,1), (10,0), rowspan = 8, colspan = 1)
        
        ax1.plot(self.data.Close, linewidth = 2.5, color = 'skyblue', label = 'Kağıt')
        ax1.plot(self.data.index, self.__buy_price, marker = '^', markersize = 10, color = 'green', label = 'AL')
        ax1.plot(self.data.index, self.__sell_price, marker = 'v', markersize = 10, color = 'r', label = 'SAT')
        ax1.set_title('RSI Indikatörü')
        ax2.plot(self.data['RSI_14'], color = 'orange', linewidth = 2.5)
        ax2.axhline(30, linestyle = '--', linewidth = 1.5, color = 'grey')
        ax2.axhline(70, linestyle = '--', linewidth = 1.5, color = 'grey')
        plt.show()
    
    def showData(self):
        self.__obtainRSI()
        print("--------")
        print(self.data.head(10))







