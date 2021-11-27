import numpy as np
import pandas as pd

class AlgoManager():
    def __init__(self):
        print("Algorithm Manager has invoke.")
        self.flag = True
        self.position_list_safe_rsi = []

    def initializeAlgoManager(self, dataframe):
        self.df = dataframe.copy()
        self.position_rsi_list = []
        self.position_self_rsi_list = []
       

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

    def startSelfRSI(self, position_list):
        self.__position_of_safe_rsi_df = self.df[["Date", "Close"]]
        self.__position_of_safe_rsi_df.reset_index(drop = True, inplace = True)

        self.position_list_safe_rsi = position_list
        print(position_list)
        if (len(self.position_list_safe_rsi) == len(self.__position_of_safe_rsi_df)):
            print('column match is ok.\nbuy:-1\nsell:1')
            print('Using Algorithm: Self RSI')
            positionDF = pd.DataFrame(self.position_list_safe_rsi, columns=["position"])
            self.__position_of_safe_rsi_df = pd.concat([self.__position_of_safe_rsi_df, positionDF], axis = 1)     

    def useSafeSell(self, dataframe):
        pass    

    def getOnlyRsiData(self):
        return self.__position_of_rsi_df

    def getOnlySelfRsiData(self):
        return self.__position_of_safe_rsi_df

    def set_safe_rsi_position_list(self, position_list):
        self.position_list_safe_rsi = position_list

    def get_safe_rsi_position_list(self):
        return self.position_list_safe_rsi


