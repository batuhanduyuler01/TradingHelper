import numpy as np
import pandas as pd

class AlgoManager():
    def __init__(self):
        print("Algorithm Manager has invoke.")

    def initializeAlgoManager(self, dataframe):
        self.df = dataframe.copy()
        self.position_rsi_list = []


    def startMacd(self):
        self.macd_df = self.df[["Date", "Macd_Buy_Position", "Macd_Sell_Position"]]

    def startRSI(self):
        self.__position_of_rsi_df = self.df[["Date", "Close"]]
        self.__position_of_rsi_df.reset_index(drop = True, inplace = True)

        for indeks, row in  self.df.iterrows() :
            if (row["RSI_Buy_Position"] > 0.0):
                self.position_rsi_list.append(-1)
            elif  (row["RSI_Sell_Position"] > 0.0):
                self.position_rsi_list.append(1)
            else:
                self.position_rsi_list.append(0)

        if (len(self.position_rsi_list) == len(self.__position_of_rsi_df)):
            print('column match is ok.\nbuy:-1\nsell:1')
            print('Using Algorithm: RSI')
            positionDF = pd.DataFrame(self.position_rsi_list, columns=["position"])
            self.__position_of_rsi_df = pd.concat([self.__position_of_rsi_df, positionDF], axis = 1)     


    def getOnlyRsiData(self):
        return self.__position_of_rsi_df



