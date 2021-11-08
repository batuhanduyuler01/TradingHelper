from datetime import date

from numpy.lib.polynomial import _polyfit_dispatcher
import Database_class as db
import IndicatorManager_class as im
import algorithm_manager_class as am
import backtest_class as backtest



class PredictionManager:
    
    def __init__(self, stockName, period, interval):
        """
        self.DataBase = db.DataBase()
        self.DataBase.insertTable("../past_work/Veri_Setleri/GARANIS.csv", "garanti")
        """
        self.indicatorManager = im.IndicatorManager(stockName = stockName, period = period, interval = interval)
        self.algoManager  = am.AlgoManager()

    def startTrading(self):
        self.algoManager.initializeAlgoManager(self.indicatorManager.getPrintableDf())
        self.algoManager.startRSI()

    def printTradings(self, rowNumber = 30):
        #self.indicatorManager.printCommonDataFramewithClose(rowNumber)
        self.indicatorManager.printOnlyTradings(rowNumber)
        self.indicatorManager.printCommonDataFramewithClose(1)

    def getTradings(self):
        return self.indicatorManager.getTradingDf()
"""
userInput = input("Market İsmini Girin: ")
#userInput = 'CANTE.IS'
predictionManager = PredictionManager(userInput.upper(), '5d', '1m')
print(f'Oynanan Market: {userInput}')
predictionManager.startTrading()
rsi_backTest = predictionManager.algoManager.getOnlyRsiData()
myBackTest = backtest.BackTesting(rsi_backTest, 1000)
myBackTest.implementBackTest()

print("\n\n\n")
#predictionManager.printTradings()
df = predictionManager.getTradings()
df.reset_index(drop = True, inplace = True)
print(df.tail(30))
"""
# use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        #period = "ytd",

# fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        #interval = "1m",

