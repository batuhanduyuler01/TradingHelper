from datetime import date

from numpy.lib.polynomial import _polyfit_dispatcher
import Database_class as db
import IndicatorManager_class as im



class PredictionManager:
    
    def __init__(self, stockName, period, interval):
        """
        self.DataBase = db.DataBase()
        self.DataBase.insertTable("../past_work/Veri_Setleri/GARANIS.csv", "garanti")
        """
        self.indicatorManager = im.IndicatorManager(stockName = stockName, period = period, interval = interval)

    def helpTrading(self, rowNumber = 30):
        self.indicatorManager.findOnlyTradings()
        self.indicatorManager.printCommonDataFramewithClose()
        self.indicatorManager.printOnlyTradings(rowNumber)
        self.indicatorManager.getFinalDate()




predictionManager = PredictionManager('GARAN.IS', '1y', '1d')
predictionManager.helpTrading()