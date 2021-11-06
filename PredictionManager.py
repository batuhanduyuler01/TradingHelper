from datetime import date
import Database_class as db
import AlgorithmicTrading_class as algoManager



class PredictionManager:
    
    def __init__(self, stockName, period, interval):
        """
        self.DataBase = db.DataBase()
        self.DataBase.insertTable("../past_work/Veri_Setleri/GARANIS.csv", "garanti")
        """
        self.algorithmHelper = algoManager.AlgorithmManager(stockName = stockName, period = period, interval = interval)

    def helpTrading(self, rowNumber = 30):
        self.algorithmHelper.findOnlyTradings()
        self.algorithmHelper.printDataFrame(rowNumber)
        self.algorithmHelper.printOnlyTradings(rowNumber)
        self.algorithmHelper.getFinalDate()




predictionManager = PredictionManager('ETH-USD', '1y', '1d')
predictionManager.helpTrading()