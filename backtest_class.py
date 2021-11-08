import numpy as np
import pandas as pd

class BackTesting():
    def __init__(self, dataframe, investmentValue = 1000):
        self.df = dataframe.copy()
        self.firstInvestmentVal = investmentValue
        self.investmentValue = investmentValue
        self.stockNumber = 0
        self.decisionFlag = False
        self.yuzdelikDurum = 0
        self.girisTarihi = str(self.df['Date'][0])
        self.cikisTarihi = str(self.df['Date'][len(self.df) - 1])


    def implementBackTest(self):
        self.stockNumber = round(self.investmentValue / self.df['Close'][0])
        for i in range(1, len(self.df)):
            if (self.df['position'][i] != 0):
                if (self.decisionFlag == False):
                    if (self.df['position'][i] == -1):
                        self.decisionFlag = True
                    elif(self.df['position'][i] == 1):
                        self.decisionFlag = True
                        self.investmentValue = self.df['Close'][i] * self.stockNumber
                        self.stockNumber = 0
                else:
                    if (self.df['position'][i] == -1):
                        #alım yap.
                        self.stockNumber = round(self.investmentValue / self.df['Close'][i])
                        self.investmentValue = 0
                    elif (self.df['position'][i] == 1):
                        #satış yap.
                        self.investmentValue = self.df['Close'][i] * self.stockNumber
                        self.stockNumber = 0
        if (self.investmentValue == 0):
            self.investmentValue = self.df['Close'][len(self.df) - 1] * self.stockNumber
            self.stockNumber = 0

    def printResults(self):
        print(f'Markete Giriş Tarihi: {self.girisTarihi}')
        print(f'Markete Girdiğiniz Para Miktari: {self.firstInvestmentVal}\n')
        print(f'Marketten Çıkış Tarihiniz: {self.cikisTarihi}')
        print(f'Marketten Çıkarkenki Para Miktarı: {self.investmentValue}')
        self.yuzdelikDurum = (self.investmentValue - self.firstInvestmentVal) / (self.firstInvestmentVal)
        print(f'Yüzdelik Durum: {self.yuzdelikDurum * 100}%')

    def getGirisTarihi(self):
        return str(self.girisTarihi)
    def getCikisTarihi(self):
        return str(self.cikisTarihi)
    def getResults(self):
        self.yuzdelikDurum = 100 * (self.investmentValue - self.firstInvestmentVal) / (self.firstInvestmentVal)
        return self.firstInvestmentVal, self.investmentValue, self.yuzdelikDurum
    
