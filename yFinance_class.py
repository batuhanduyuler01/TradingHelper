import numpy as np
import pandas as pd
#Data Source
import yfinance as yf

class yFinance :
    def __init__(self, stockName = 'ETH-USD', periodNo = "1d", intervalNo = "1m"):
        self.df = yf.download(tickers= stockName, period = periodNo, interval = intervalNo)
        self.df = self.df.rename_axis('Date').reset_index()

    def getData(self):
        return self.df

# use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        #period = "ytd",

# fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        #interval = "1m",


