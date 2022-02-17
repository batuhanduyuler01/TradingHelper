import pandas as pd
import numpy as np


class DataProcessor: 
    def __init__(self, dataframe):
        self.__df = pd.DataFrame()
        self.__labeledDf = pd.DataFrame()
        self.isLabeled = False
        self.__df = dataframe.copy()


    def obtain_trend_label(self):
        if (False ==  self.isLabeled):

            labels = []
            numberOfDays = len(self.__df)

            for day in range(0, numberOfDays - 1):
                temporaryTrend = np.sign(self.__df["Close"][day+1] - self.__df["Close"][day])
                if (temporaryTrend == 0):
                    temporaryTrend = 1

                labels.append(temporaryTrend)

            #100 gün olsun. En son 99.günün indeksini öğrendiğimiz için 100.günü drop ediyoruz.
            newDataframe = self.__df.drop(index = self.__df.index[-1])
            newDataframe.insert(newDataframe.shape[1], "Label", labels, True)
            self.isLabeled = True
            self.__labeledDf = newDataframe.copy()
            return newDataframe
        else :
            return self.__labeledDf


    def fill_missing_volumes(self, dataframe):
        df = dataframe.copy()

        volumeChange = 0

        for indx, row in df.iterrows():
            dummyCondition = False
            volumeCondition = False

            if row["Volume"] == 0:
                volumeCondition = True
            if row["Open"] == row["Close"] == row["High"] == row["Low"]:
                dummyCondition = True

            if (volumeCondition and dummyCondition):
                df.drop(axis = 0, index = indx, inplace = True)
            elif (dummyCondition == False and volumeCondition == True):
                volumeChange += 1

                if (indx != 0 and indx != 1): #indx < 1
                    newVolume = (df["Volume"][indx-2 : indx+2]).mean()
                    df.at[indx, "Volume"] = newVolume
                else:
                    newVolume = (df["Volume"][indx:indx+4]).mean()
                    df.at[indx, "Volume"] = newVolume

        return (df.reset_index(drop = True))

    def set_date(self, inputDate):
        df = pd.DataFrame()

        if (self.isLabeled):
            df = self.__labeledDf.copy()
        else:
            df = self.__df.copy()

        if (inputDate > max(df["Date"])):
            raise AssertionError()

        else:
            #datasette, bu tarihe eşit ve sonraki tarihleri tüm kolonlarla al
            df = df[df.Date >= inputDate]
            df = df.reset_index(drop = True) 
            
        return df

