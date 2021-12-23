from functools import singledispatch
from numpy.lib.function_base import append
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.series import Series 
import yFinance_class as yf

class safeCellRSI:
    def __init__(self, dataframe, date = '2019-01-01', lookback = 7, expectedProfit = 0.1):
        # Initialize Dataframe Parameters
        #self.data = pd.read_csv("../past_work/Veri_Setleri/GARAN.IS.csv")
        self.data = dataframe.copy()
        self.data = self.data[self.data.Date > str(date)]
        self.data = self.data.set_index(pd.DatetimeIndex(self.data['Date'].values))
        self.df_RSI = pd.DataFrame()
        self.lower_band = 50.0
        self.upper_band = 85.0
        self.lastBuyPrice = []

        # Initialize Strategy Parameters
        self.__buy_price = []
        self.__sell_price = []
        self.rsi_signal = []
        self.signal = 0
        self.lookback = lookback
        self.beklenenKar = expectedProfit

    def getSellPriceInfo(self):
        return self.__sell_price
    def getBuyPriceInfo(self):
        return self.__buy_price

    def wait_for_signal(self, buyList, sellList, signalList):
        buyList.append(np.nan)
        sellList.append(np.nan)
        signalList.append(0)

    def fill_buy_signal(self, buyList,buyPrice, sellList, signalList):
        buyList.append(buyPrice)
        sellList.append(np.nan)
        signalList.append(1)
        
    def fill_sell_signal(self, buyList, sellList, sellPrice, signalList):
        buyList.append(np.nan)
        sellList.append(sellPrice)
        signalList.append(-1)

    def __obtainRSI(self):
        close = self.data.Close #self.prices ile değiştirilebilir ileride
        ret = close.diff()
        up = []
        down = []

        for element in range(0, len(ret)):
            if (ret[element] < float(0)):
                up.append(0)
                down.append(ret[element])
            elif (ret[element] >= float(0)):
                up.append(ret[element])
                down.append(0)
    
        upSeries = pd.Series(up)
        downSeries = pd.Series(down).abs()

        ret = ret.replace(np.nan, 0)

        upEwm = upSeries.ewm(com = self.lookback - 1, adjust = False).mean()
        downEwm = downSeries.ewm(com = self.lookback - 1, adjust = False).mean()
        rs = upEwm / downEwm
        rsi = 100 - (100 / (1 + rs))
            #diff aldığımız için ilk elemana karşılık gelen ret boşta kalıyor
            #RSI hesaplarında n gün varsa (n-1) RSI değeri elde etmiş oluyoruz
            #bu nedenle ilk indeksi dropluyoruz
        close = close.drop(index = close.index[0])
        temp_df = pd.DataFrame(rsi).rename(columns={0 : 'rsi'}).set_index(close.index)
        self.data['RSI_14'] = temp_df[2:]

    def implementStrategy(self):
        self.__obtainRSI()
        rsi = self.data.RSI_14
        prices = self.data.Close

        for element in range(1, len(rsi)):
            if ((rsi[element - 1] > self.lower_band) and (rsi[element] < self.lower_band)):
                #eğer rsi değeri 50'un üstünden 50'un altına geçiş yaptıysa
                #alım yapmak istiyoruz
                #ancak iki kere alım yapamayacağımızdan sinyal kontrolü yap.
                if (self.signal != 1):
                    self.fill_buy_signal(self.__buy_price, prices[element], self.__sell_price, self.rsi_signal)
                    self.signal = 1
                    self.lastBuyPrice.append(prices[element])
                else:
                    #RSI alım sinyali verdi ama zaten alım yapmışız
                    #fakat karımız %5 üzerindeyse satış yapmak istiyoruz.
                    #o yüzden ilk önce fiyat düşüşte mi ona bakıyoruz
                    if (prices[element - 1] > prices[element]):
                        #eğer düşüşteyse aldığımız fiyattan yüksek mi
                        #onu kontrol etmeliyiz.
                        if (prices[element] > self.lastBuyPrice[-1]):
                            #eğer öyleyse karımızı hesaplamalıyız
                            lossPortion = (prices[element] - self.lastBuyPrice[-1]) / self.lastBuyPrice[-1]
                            if (lossPortion > self.beklenenKar ):
                                print(lossPortion)
                                self.fill_sell_signal(self.__buy_price, self.__sell_price, prices[element], self.rsi_signal)
                                self.signal = -1
                            else:
                                self.wait_for_signal(self.__buy_price, self.__sell_price, self.rsi_signal)
                        else:
                            self.wait_for_signal(self.__buy_price, self.__sell_price, self.rsi_signal)
                    else:
                        self.wait_for_signal(self.__buy_price, self.__sell_price, self.rsi_signal)
                    
            elif((rsi[element - 1] < self.upper_band) and (rsi[element] > self.upper_band)):
                #eğer rsi değeri 70'in altındaysa ve 70'in üstüne geçiş yaptıysa
                #satış yapmak istiyoruz
                #ancak iki kere satış yapamacağımızdan sinyal kontrolü yap
                if (self.signal != -1):
                    self.fill_sell_signal(self.__buy_price, self.__sell_price, prices[element], self.rsi_signal)
                    self.signal = -1
                else:
                    self.wait_for_signal(self.__buy_price, self.__sell_price, self.rsi_signal)
                #satış pozisyonunda bir daha satış yapamayacağımızdan burayı pass geçiyoruz.   
            else:
                #eğer bu durumlardan biri yaşanmadıysa, karı kontrol edebiliriz.
                #ilk olarak sinyal alım pozisyonunda mı ona bakıyoruz.
                if (self.signal == 1):
                    if (prices[element - 1] > prices[element]):
                        #fiyat düşüştüyse tespit ettik.
                        if (prices[element] > self.lastBuyPrice[-1]):
                            #karda olup olmadığımızı kontrol ettik
                            lossPortion = (prices[element] - self.lastBuyPrice[-1]) / self.lastBuyPrice[-1]
                            if (lossPortion > self.beklenenKar):
                                print(lossPortion)
                                self.fill_sell_signal(self.__buy_price, self.__sell_price, prices[element], self.rsi_signal)
                                self.signal = -1
                            else:
                                self.wait_for_signal(self.__buy_price, self.__sell_price, self.rsi_signal)
                        else:
                            self.wait_for_signal(self.__buy_price, self.__sell_price, self.rsi_signal)
                    else:
                        self.wait_for_signal(self.__buy_price, self.__sell_price, self.rsi_signal)
                else:
                    self.wait_for_signal(self.__buy_price, self.__sell_price, self.rsi_signal)
    
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
    
    
    def obtain_strategy_df(self):
        temp_df = pd.DataFrame(list(zip(self.data.Date[1:].to_list(), self.data.Close[1:].to_list(), self.rsi_signal)), columns = ["Date", "Close", "Signal"])
        return temp_df

    def getPositionList(self):
        return self.rsi_signal
    
    def showData(self):
        self.__obtainRSI()
        print("--------")
        print(self.data.tail(10))







