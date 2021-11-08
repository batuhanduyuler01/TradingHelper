import PredictionManager as pm #this import will be replaced with user context
import streamlit as st
import backtest_class as backtest


stockList = ["None", "KARSN.IS", "GARAN.IS", "CANTE.IS", "ALGO-USD", "AVAX-USD", "TSLA", "SHIB-USD", "BTC-USD", "ETH-USD"]
predictionIntervalList = ["None", "1d", "1wk"] #1minute oldugunda rsi calculation hatası alıyoruz. sadece webapp'te.
backTestIntervalList = ["None", "3mo", "1y"]


def main():
    st.header("Borsa - Kripto Borsa Trading Helper")

    stockChoice = st.sidebar.selectbox("Hisse Seçiniz", stockList)
    predictionInterval = st.sidebar.selectbox("Tahmin Aralığı Seçiniz", predictionIntervalList)
    backtestInterval = st.sidebar.selectbox("BackTest: Ne zamandır bu kağıttasınız: ", backTestIntervalList)

    st.subheader("Tahminleri görmeden önce hisse ve tahmin seçeneğinizi belirleyin.\nSonrasında tahminleri getir seçeneğine tıklayın.")
    bringPredictions = st.checkbox("Tahminleri Getir")

    if (bringPredictions):
        if ((predictionInterval != "None") and (stockChoice != "None")):
            predictionManager = pm.PredictionManager(stockChoice, '1y', predictionInterval)
            predictionManager.startTrading()
            tempDataframe = predictionManager.getTradings()
            tempDataframe["Date"] = tempDataframe["Date"].astype(str)
            tempDataframe.reset_index(drop = True, inplace = True)
            st.write("Son 10 Tahmin:")
            st.table(tempDataframe.tail(10))
            st.subheader("\nSon tahmin: ")
            st.table(tempDataframe.tail(1))
            
            st.subheader('RSI Stratejisine Göre BackTest Uygula \nSol sekmeden ne kadar süre önce hisseye girmiş olmak istediğini seçin.')
            startBackTest = st.checkbox("Testi Uygula")
            if (startBackTest):
                if (backtestInterval != "None"):
                    backtestManager = pm.PredictionManager(stockChoice, backtestInterval, predictionInterval)
                    backtestManager.startTrading()
                    rsiBackTest = backtestManager.algoManager.getOnlyRsiData()
                    myBackTest = backtest.BackTesting(rsiBackTest, 1000)
                    myBackTest.implementBackTest()

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
                    st.write("Lütfen Hisseye Kaç Ay Önce Gireceğinizi Seçin ve Testi Tekrar Başlatın")
    



if __name__ == "__main__":
    main()
