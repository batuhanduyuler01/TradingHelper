from pandas.core.indexing import maybe_convert_ix
import PredictionManager as pm
import backtest_class as backTest

class UserContext():
    def __init__(self):
        #userInput = input("Market İsmini Girin: ")
        self.userInput = "AVAX-USD"
        self.period = '1y'
        self.interval = '1d'

        self.predictionManager = pm.PredictionManager(self.userInput.upper(), self.period, self.interval)
        print(f'Oynanan Market: {self.userInput.upper()}')

    def useSafeSell(self, dataframe):
        self.safeSellDataframe = dataframe.copy()
        self.predictionManager.algoManager.useSafeSell(self.safeSellDataframe)        




userContext = UserContext()
userContext.predictionManager.startSafeTrading(userContext.predictionManager.indicatorManager.getSafeSell().getPositionList())
safeRSI = userContext.predictionManager.algoManager.getOnlySelfRsiData()
print(safeRSI.position.unique())
myBackTest = backTest.BackTesting(safeRSI, 1000)
myBackTest.implementBackTest()


print("Hisseye Giris Tarihi: ", myBackTest.getGirisTarihi())
print("Hisseden Cikis Tarihi: ", myBackTest.getCikisTarihi())
firstInvestment, finalResult, yuzdelikDurum = myBackTest.getResults()
print("İlk yatırım miktarı: ", firstInvestment)
print("Son gün satış sonrası durum: ", finalResult)
print(yuzdelikDurum)

"""
userContextRSI = UserContext()
userContextRSI.predictionManager.startTrading()
rsiBackTest = userContextRSI.predictionManager.algoManager.getOnlyRsiData()
mySecondTest = backTest.BackTesting(rsiBackTest, 1000)
mySecondTest.implementBackTest()

print("Hisseye Giris Tarihi: ", mySecondTest.getGirisTarihi())
print("Hisseden Cikis Tarihi: ", mySecondTest.getCikisTarihi())
firstInvestment, finalResult, yuzdelikDurum = mySecondTest.getResults()
print("İlk yatırım miktarı: ", firstInvestment)
print("Son gün satış sonrası durum: ", finalResult)
print(yuzdelikDurum)
"""


"""
                    backtestManager = pm.PredictionManager(stockChoice, backtestInterval, predictionInterval)
                    backtestManager.startTrading()
                    rsiBackTest = backtestManager.algoManager.getOnlyRsiData()
                    myBackTest = backtest.BackTesting(rsiBackTest, 1000)
                    myBackTest.implementBackTest()
"""