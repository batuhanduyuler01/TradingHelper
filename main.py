############################################
# Bu dosya, projede yapılan                #
# ufak değişikliklerin test edilmesi       #
# için oluşturulmuştur.                    #
############################################


from pandas.core.indexing import maybe_convert_ix
import PredictionManager as pm
import backtest_class as backTest



userInput = "CANTE.IS"
period = '1y'
interval = '60m'
myPredictions = pm.PredictionManager(userInput.upper(), period, interval)
myPredictions.indicatorManager.set_strategy_df_all()