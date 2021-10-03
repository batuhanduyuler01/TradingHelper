import MACD_class as macd
import RSI_class as rsi
import Database_class as db
import Bollinger_class as bb


class PredictionManager:
    
    def __init__(self):
        self.DataBase = db.DataBase()
        self.DataBase.insertTable("../past_work/Veri_Setleri/GARANIS.csv", "garanti")
        #self.DataBase.printCSV("garanti")
        self.MACD = macd.MACD(dataframe = self.DataBase.getTable())
        self.RSI = rsi.RSI(dataframe = self.DataBase.getTable())
        self.BB = bb.Bollinger(dataframe = self.DataBase.getTable())
        

PM = PredictionManager()
PM.BB.plotStrategy()

