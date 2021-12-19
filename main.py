############################################
# Bu dosya, projede yapılan                #
# ufak değişikliklerin test edilmesi       #
# için oluşturulmuştur.                    #
############################################


from pandas.core.indexing import maybe_convert_ix
import PredictionManager as pm
import backtest_class as backTest


userInput = "SOL1-USD"
period = '1y'
interval = '1d'
myPredictions = pm.PredictionManager(userInput.upper(), period, interval)
myPredictions.indicatorManager.set_strategy_df_all()