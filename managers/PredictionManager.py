import sys
sys.path.insert(0, '../helpers/')



from datetime import date

from numpy.lib.polynomial import _polyfit_dispatcher
import helpers.Database_class as db
import managers.IndicatorManager_class as im
import managers.algorithm_manager_class as am
import helpers.backtest_class as backtest



class PredictionManager:
    
    def __init__(self, stockName, period, interval):
        """
        self.DataBase = db.DataBase()
        self.DataBase.insertTable("../past_work/Veri_Setleri/GARANIS.csv", "garanti")
        """
        self.indicatorManager = im.IndicatorManager(stockName = stockName, period = period, interval = interval)


