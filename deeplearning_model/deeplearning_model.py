import sys
sys.path.insert(0, '../../current_work')


import yFinance_class as yfHelper

# Veri Çekme İşlemleri #
# 1 - Tüm data için aynı period ve interval almak istiyoruz.
# use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        #period = "ytd",

# fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        #interval = "1m",

period = '60m'
interval = '2y'

userInputStock = 'GARAN.IS'
userInputStockRelated = 'YKBNK.IS'
userInputBIST = 'XU030.IS'
userInputUSD_TRY = 'TRY=X'
userInputJapanese30 = '^N225'

stockData = yfHelper.yFinance(userInputStock.upper(), period, interval).getData()
stockHelperData_0 = yfHelper.yFinance(userInputStockRelated.upper(), period, interval).getData()
stockHelperData_1 = yfHelper.yFinance(userInputUSD_TRY.upper(), period, interval).getData()
stockHelperData_2 = yfHelper.yFinance(userInputBIST.upper(), period, interval).getData()
stockHelperData_3 = yfHelper.yFinance(userInputJapanese30.upper(), period, interval).getData()


print(len(stockData))