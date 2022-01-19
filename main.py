############################################
# Bu dosya, projede yapılan                #
# ufak değişikliklerin test edilmesi       #
# için oluşturulmuştur.                    #
############################################


from pandas.core.indexing import maybe_convert_ix
import PredictionManager as pm
import backtest_class as backTest
import algorithm_manager_class as algoManager
import e_mail_report.e_mail_module as mailConsumer

# use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        #period = "ytd",

# fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        #interval = "1m",

userInput = "ASELS.IS"
period = '3mo'
interval = '1d'
myPredictions = pm.PredictionManager(userInput.upper(), period, interval)


onlyTradings = myPredictions.indicatorManager.findOnlyTradingsNew(True)
print(onlyTradings.head(50))

#TODO: batuhan.duyuler: bu veri seti ayrımlarını nerede yapmalıyız karar ver
genelVeri = myPredictions.indicatorManager.get_strategy_df_all()

rsi_df = genelVeri[["Date", "RSI", "Close"]]
macd_df = genelVeri[["Date", "MACD", "Close"]]
rsi_safe_df = genelVeri[["Date", "RSI_Safe", "Close"]]
bollinger_df = genelVeri[["Date", "BollingBand", "Close"]]

myBackTest = backTest.BackTesting(rsi_safe_df)
myBackTest.implementBackTestNew()
myBackTest.printResults()

myAlgoManager = algoManager.AlgoManager()
myAlgoManager.initializeAlgoManager(userInput, period, interval)
myAlgoManager.startProcess()

newMail = mailConsumer.eMailSender()
receiverAddress = "batuhanduyuler@gmail.com"
# newMail.send_mail(receiverAddress, "Selamun Aleykum Kardes, Bu Mail bir test mailidir.")
htmlMsg = "Selamlar !\n"
newMail.send_mail_with_html_buffer(receiverAddress, htmlMsg)

