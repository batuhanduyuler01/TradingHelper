from datetime import date
import MACD_class as macd
import RSI_class as rsi
import Database_class as db
import Bollinger_class as bb
import yFinance_class as yfHelper


class PredictionManager:
    
    def __init__(self):
        self.DataBase = db.DataBase()
        self.DataBase.insertTable("../past_work/Veri_Setleri/GARANIS.csv", "garanti")

    def helpTrading(self, stockName, period, interval):
        self.yData = yfHelper.yFinance(stockName, period , interval)
        self.bollinger = bb.Bollinger(self.yData.getData(), date='2015-01-01')
        self.bollinger.plotStrategy()
        self.macd = macd.MACD(self.yData.getData(), date = '2015-01-01')
        self.macd.plotStrategy()
        self.rsi = rsi.RSI(self.yData.getData(), date = '2015-01-01')
        self.rsi.plotStrategy()
        

predictionManager = PredictionManager()
predictionManager.helpTrading('AAPL', '2y', '1d')
