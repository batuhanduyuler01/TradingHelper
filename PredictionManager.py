import MACD_class as macd
import RSI_class as rsi


class PredictionManager:
    
    def __init__(self):
        self.MACD = macd.MACD()
        self.RSI = rsi.RSI()

PM = PredictionManager()
PM.RSI.showData()

PM.RSI.plotStrategy()