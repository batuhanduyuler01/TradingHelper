import PredictionManager as pm #this import will be replaced with user context
import streamlit as st
import backtest_class as backtest
import pandas as pd

# use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        #period = "ytd",

# fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        #interval = "1m",

stockList = ["None", "KARSN.IS", "GARAN.IS", "CANTE.IS", "ALGO-USD", "AVAX-USD", "TSLA", "SHIB-USD", "BTC-USD", "ETH-USD", "SASA.IS"]
predictionIntervalList = ["None", "1m", "2m" , "5m" ," 15m" ," 30m" ,"60m" ," 90m" ,"1h" ," 1d" ,"5d" ," 1wk" ,"1mo" ,"3mo"]
predictionPeriodList = ["None", "1d", "5d", "1mo" , "3mo" , "6mo" ," 1y" ," 2y" ," 5y" ,"10y" ]  #TODO: batuhan.duyuler: 1minute oldugunda rsi calculation hatası alıyoruz. sadece webapp'te.


def main():
    st.header("Borsa - Kripto Borsa Trading Helper")

    stockChoice = st.sidebar.selectbox("Hisse Seçiniz", stockList)
    predictionInterval = st.sidebar.selectbox("Tahmin Aralığı Seçiniz", predictionIntervalList)
    predictionPeriod = st.sidebar.selectbox("Tahmin Periyodu Giriniz", predictionPeriodList)

    st.subheader("Tahminleri görmeden önce hisse ve tahmin seçeneğinizi belirleyin.\nSonrasında tahminleri getir seçeneğine tıklayın.")
    bringPredictions = st.checkbox("Tahminleri Getir")

    if (bringPredictions):
        if ((predictionInterval != "None") and (stockChoice != "None") and (predictionPeriod != "None")):
            predictionManager = pm.PredictionManager(stockChoice, predictionPeriod, predictionInterval)
            onlyTradings = predictionManager.indicatorManager.findOnlyTradingsNew(True)

            onlyTradings["Date"] = onlyTradings["Date"].astype(str)
            # onlyTradings = onlyTradings.set_index(pd.DatetimeIndex(onlyTradings['Date'].values))
            # onlyTradings = onlyTradings.drop(["Date"], axis = 1)
            onlyTradings = onlyTradings.replace(1, 'AL')
            onlyTradings = onlyTradings.replace(-1, 'SAT')
            onlyTradings = onlyTradings.replace(0 , '-')

            
            if (len(onlyTradings) > 9):
                st.write("Son 10 Tahmin:")
                st.table(onlyTradings.tail(10))
            else:
                st.write("10 tahmin icermemektedir.")
            if (len(onlyTradings) > 0):
                st.subheader("\nSon tahmin: ")
                st.table(onlyTradings.tail(1))
            else:
                st.write("tahmin icermemektedir.")
            
    st.subheader('Stratejisine Göre BackTest Uygulamak İçin \nSeçenekleri Görün')
    startBackTest = st.checkbox("Seçenekleri Gör")
    if ((predictionInterval != "None") and (stockChoice != "None") and (predictionPeriod != "None")):
        if (startBackTest):
            myPredictions = pm.PredictionManager(stockChoice, predictionPeriod, predictionInterval)
            genelVeri = myPredictions.indicatorManager.get_strategy_df_all()

            rsiSafeBackTest = st.checkbox("RSI Safe Sell")
            macdBackTest = st.checkbox("MACD Back Test")
            bollingerBackTest = st.checkbox("Bollinger Band Back Test")
            onlyRSIBackTest = st.checkbox("RSI Back Test")
            if (rsiSafeBackTest):
                rsi_safe_df = genelVeri[["Date", "RSI_Safe", "Close"]]
                myBackTest = backtest.BackTesting(rsi_safe_df)
                myBackTest.implementBackTestNew()

                st.write("Uygulanan Strateji: RSI Safe Sell")
                st.write("Hisseye Giris Tarihi: ", myBackTest.getGirisTarihi())
                st.write("Hisseden Cikis Tarihi: ", myBackTest.getCikisTarihi())
                firstInvestment, finalResult, yuzdelikDurum = myBackTest.getResults()
                st.write("İlk yatırım miktarı: ", firstInvestment)
                st.write("Son gün satış sonrası durum: ", finalResult)
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
                st.write("İlk yatırım miktarı: ", firstInvestment)
                st.write("Son gün satış sonrası durum: ", finalResult)
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
                st.write("İlk yatırım miktarı: ", firstInvestment)
                st.write("Son gün satış sonrası durum: ", finalResult)
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
                st.write("İlk yatırım miktarı: ", firstInvestment)
                st.write("Son gün satış sonrası durum: ", finalResult)
                if (yuzdelikDurum < 0):
                    st.write("Yüzdelik Durum: %", yuzdelikDurum, " zarar")
                else:
                    st.write("Yüzdelik Durum: %", yuzdelikDurum, " kar")
    else:
        st.write("Lutfen Interval - Period - Kagit İsmi Giriniz")


    



if __name__ == "__main__":
    main()
