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

