import managers.PredictionManager as pm #this import will be replaced with user context
import streamlit as st
import helpers.backtest_class as backtest
import managers.algorithm_manager_class as algoManager
import pandas as pd

# use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        #period = "ytd",

# fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        #interval = "1m",

stockList = ["None", "KARSN.IS", "GARAN.IS", "CANTE.IS", "THYAO.IS", "SASA.IS", "AKBNK.IS", "ARCLK.IS", "GUBRF.IS", "PGSUS.IS", "SISE.IS", "TUPRS.IS", "PETKM.IS"]
predictionIntervalList = ["None", "1m", "5m" ," 15m" ," 30m","1h" ," 1d" ," 1wk" ,"1mo"]
predictionPeriodList = ["None", "1d","1mo" , "3mo" , "6mo" ," 1y" ," 2y" ," 5y" ]
algoList = ["None", "MACD", "RSI_Safe_Sell", "Bollinger", "RSI"] 
def app():

    stockCol1, stockCol2 = st.columns(2)
    stockChoice = stockCol1.selectbox(" Sık Kullanılan Coinler", stockList)
    title = stockCol2.text_input('Farklı bir coin için ', 'coin ismi girin...')

    intervalColumn, periodColumn = st.columns(2)
    predictionInterval = intervalColumn.selectbox("Tahmin Aralığı Seçiniz", predictionIntervalList)
    predictionPeriod = periodColumn.selectbox("Tahmin Periyodu Giriniz", predictionPeriodList)
    
    with st.expander("Tahminleri Getir"):

        buttonCol1, buttonCol2, buttonCol3 = st.columns(3)

        firstButton = buttonCol1.button("Son 10 Tahmin")
        secondButton = buttonCol2.button("Son 20 Tahmin")
        thirdButton = buttonCol3.button("Tüm Tahminler")

        if ((predictionInterval != "None") and (stockChoice != "None" or title != "coin ismi girin...") and (predictionPeriod != "None")):

            if (stockChoice != "None"):
                finalValueManager = pm.PredictionManager(stockChoice, "1d", "1m")
                predictionManager = pm.PredictionManager(stockChoice, predictionPeriod, predictionInterval)
            
            if (title != "coin ismi girin..."):
                finalValueManager = pm.PredictionManager(title.upper(), "1d", "1m")
                predictionManager = pm.PredictionManager(title.upper(), predictionPeriod, predictionInterval)

            onlyTradings = predictionManager.indicatorManager.findOnlyTradingsNew(True)

            onlyTradings["Date"] = onlyTradings["Date"].astype(str)
            # onlyTradings = onlyTradings.set_index(pd.DatetimeIndex(onlyTradings['Date'].values))
            # onlyTradings = onlyTradings.drop(["Date"], axis = 1)
            onlyTradings = onlyTradings.replace(1, 'AL')
            onlyTradings = onlyTradings.replace(-1, 'SAT')
            onlyTradings = onlyTradings.replace(0 , '-')
            #TODO: batuhan.duyuler: find the selected strategies final prediction.  

            if (firstButton):
                if (len(onlyTradings) > 9):
                    st.write("Son 10 Tahmin:")
                    st.table(onlyTradings.tail(10))
                else:
                    st.table(onlyTradings)
                    st.write("10 tahmin icermemektedir.\nTüm tahminler: ")

            if (secondButton):
                if (len(onlyTradings) > 19):
                    st.write("Son 10 Tahmin:")
                    st.table(onlyTradings.tail(20))
                else:
                    st.table(onlyTradings)
                    st.write("20 tahmin icermemektedir.\nTüm tahminler: ")

            if (thirdButton):
                st.write("Tüm Tahminler:")
                st.table(onlyTradings)

            
            finalValue = str(round(finalValueManager.indicatorManager.yData.getData()["Close"].iloc[-1], 2))
            finalDate = str(finalValueManager.indicatorManager.yData.getData()["Date"].iloc[-1])

            if (len(onlyTradings) > 0):
                col1, col2 = st.columns((5,1))
                col1.subheader("\nSon tahmin: ")
                col1.table(onlyTradings.tail(1))
                col2.subheader("Anlık: ")
                col2.write(finalDate)
                col2.write(finalValue)
            else:
                st.write("tahmin icermemektedir.")

    st.subheader("Seçili kağıt ve aralıkta en iyi stratejiyi gör (premium :D )")
    strategy = st.checkbox("Taramayı Başlat")
    if ((predictionInterval != "None") and (stockChoice != "None" or title != "coin ismi girin...") and (predictionPeriod != "None")):
        if (strategy):
            myAlgoManager = algoManager.AlgoManager()
            myAlgoManager.initializeAlgoManager(stockChoice, predictionPeriod, predictionInterval)
            myAlgoManager.startProcess()
            strategyName, bestProfit = myAlgoManager.getBestStrategy()

            st.write("En iyi strateji: ", strategyName)
            if (bestProfit < 0):
                st.write("Yuzdelik Durum: %", bestProfit, "zarar")
            else:
                st.write("Yuzdelik Durum: %", bestProfit, "kar")
                st.write("BaranDenizDeneme")

    with st.sidebar.expander("Back Test Analizi"):
        rsiSafeBackTest = st.checkbox("RSI Safe")
        macdBackTest = st.checkbox("MACD")
        bollingerBackTest = st.checkbox("Bollinger Band")
        onlyRSIBackTest = st.checkbox("RSI")
        
        if ((predictionInterval != "None") and (stockChoice != "None" or title != "coin ismi girin...") and (predictionPeriod != "None")):
                genelVeri = predictionManager.indicatorManager.get_strategy_df_all()

                if (rsiSafeBackTest):
                    rsi_safe_df = genelVeri[["Date", "RSI_Safe", "Close"]]
                    myBackTest = backtest.BackTesting(rsi_safe_df)
                    myBackTest.implementBackTestNew()

                    st.write("Uygulanan Strateji: RSI Safe Sell")
                    st.write("Hisseye Giris Tarihi: ", myBackTest.getGirisTarihi())
                    st.write("Hisseden Cikis Tarihi: ", myBackTest.getCikisTarihi())
                    firstInvestment, finalResult, yuzdelikDurum = myBackTest.getResults()
                    if (yuzdelikDurum < 0):
                        st.write("Yüzdelik Durum: %", yuzdelikDurum, " zarar")
                    else:
                        st.write("Yüzdelik Durum: %", yuzdelikDurum, " kar")
                elif (macdBackTest):
                    macd_df = genelVeri[["Date", "MACD", "Close"]]
                    myBackTest = backtest.BackTesting(macd_df)
                    myBackTest.implementBackTestNew()

                    st.write("Uygulanan Strateji: MACD")
                    st.write("Hisseye Giris Tarihi: ", myBackTest.getGirisTarihi())
                    st.write("Hisseden Cikis Tarihi: ", myBackTest.getCikisTarihi())
                    firstInvestment, finalResult, yuzdelikDurum = myBackTest.getResults()
                    if (yuzdelikDurum < 0):
                        st.write("Yüzdelik Durum: %", yuzdelikDurum, " zarar")
                    else:
                        st.write("Yüzdelik Durum: %", yuzdelikDurum, " kar")
                elif (bollingerBackTest):
                    bollinger_df = genelVeri[["Date", "BollingBand", "Close"]]
                    myBackTest = backtest.BackTesting(bollinger_df)
                    myBackTest.implementBackTestNew()

                    st.write("Uygulanan Strateji: Bollinger Band")
                    st.write("Hisseye Giris Tarihi: ", myBackTest.getGirisTarihi())
                    st.write("Hisseden Cikis Tarihi: ", myBackTest.getCikisTarihi())
                    firstInvestment, finalResult, yuzdelikDurum = myBackTest.getResults()
                    if (yuzdelikDurum < 0):
                        st.write("Yüzdelik Durum: %", yuzdelikDurum, " zarar")
                    else:
                        st.write("Yüzdelik Durum: %", yuzdelikDurum, " kar")
                elif (onlyRSIBackTest):
                    rsi_df = genelVeri[["Date", "RSI", "Close"]]
                    myBackTest = backtest.BackTesting(rsi_df)
                    myBackTest.implementBackTestNew()


                    st.write("Uygulanan Strateji Düz RSI: 30-70")
                    st.write("Hisseye Giris Tarihi: ", myBackTest.getGirisTarihi())
                    st.write("Hisseden Cikis Tarihi: ", myBackTest.getCikisTarihi())
                    firstInvestment, finalResult, yuzdelikDurum = myBackTest.getResults()
                    if (yuzdelikDurum < 0):
                        st.write("Yüzdelik Durum: %", yuzdelikDurum, " zarar")
                    else:
                        st.write("Yüzdelik Durum: %", yuzdelikDurum, " kar")
        else:
            st.write("Lutfen Interval - Period - Kagit İsmi Giriniz")

    graphCol1, graphCol2 = st.columns((10,1))
    with st.sidebar.expander("Grafik Analizi"):
        grafikSecenekleri = st.selectbox("Algo: ", algoList)
        if ((predictionInterval != "None") and (stockChoice != "None" or title != "coin ismi girin...") and (predictionPeriod != "None")):
            # pManager = pm.PredictionManager(stockChoice, predictionPeriod, predictionInterval)
            if (grafikSecenekleri == "RSI"):                        
                fig = predictionManager.indicatorManager.rsi.plotStrategy()
            elif (grafikSecenekleri == "MACD"):
                fig = predictionManager.indicatorManager.macd.plotStrategy()
            elif (grafikSecenekleri == "RSI_Safe_Sell"):
                fig = predictionManager.indicatorManager.safeSellRSI.plotStrategy()
            elif (grafikSecenekleri == "Bollinger"):
                fig = predictionManager.indicatorManager.bollinger.plotStrategy()
            
            
        graphButton = st.sidebar.button("Grafik Getir")

        if (graphButton):
            if (grafikSecenekleri != "None"):
                graphCol1.pyplot(fig)
            else:
                st.write("Lutfen bi algoritma seciniz")

