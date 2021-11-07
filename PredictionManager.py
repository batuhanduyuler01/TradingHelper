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
        self.indicatorManager.printCommonDataFramewithClose(rowNumber)
        self.indicatorManager.printOnlyTradings(rowNumber)


predictionManager = PredictionManager('KARSN.IS', '1y', '1d')
#predictionManager.printTradings()
print('Oynanan Market: KARSN.IS')
predictionManager.startTrading()
rsi_backTest = predictionManager.algoManager.getOnlyRsiData()
myBackTest = backtest.BackTesting(rsi_backTest, 1000)
myBackTest.implementBackTest()
