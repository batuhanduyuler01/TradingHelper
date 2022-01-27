# -*- coding: utf-8 -*-
"""
author: batuhan
date  : 09-07-2021
"""

import DataProcessLibrary as dp
import ModelDevelopLibrary as mdl
import ModelSuccessLibrary as msl
import pandas as pd

data = pd.read_csv("../past_work/Veri_Setleri/GARAN.IS.csv")
#verisetini hangi tarihten itibaren incelemek istiyoruz
initial_date = "2018-01-01"

veriseti = dp.tarih_ayarlama(data, initial_date)
df = dp.volumeCheck(veriseti)
new_df = dp.obtainLabels(df)
new_df = dp.obtainPreviousLabel(new_df)
    


print(f"volumeCheck öncesi veri uzunluğu: {len(veriseti)}")
print(f"volumeCheck sonrası veri kaybolan veri {len(veriseti)-len(df)}")


import RSI_Library as rsi
new_df["RSI"] = rsi.obtainRSI(new_df, 14)
import MACD_Library as macd
macd_df = macd.getMACD(new_df)
new_df = pd.concat([new_df, macd_df], axis = 1)

new_df = new_df.dropna()

col_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume',
        'RSI', 'MACD', 'signal', 'hist','Previous_Label', 'Label',]

new_df = new_df.reindex(columns=col_names)

new_df  = new_df.drop(["Adj Close"], axis = 1)

#new_df.to_csv("model_data.csv", index = False)

model_data = new_df.copy()


df = mdl.minmaxScaler(model_data)

train, test = mdl.train_test_split(df,.95)

n_past = 10
n_future = 1

X_train, y_train = mdl.futureSplitData(train, n_past, n_future, 0)
X_test, y_test = mdl.futureSplitData(test, n_past, n_future, 0)

#X_train, y_train, y_label_train = mdl.splitData(train, n_past, n_future)
#X_test, y_test, y_label_test = mdl.splitData(test, n_past, n_future)

X_train, X_test = mdl.reshapeData_X(X_train, X_test)
y_train, y_test = mdl.reshapeData_y(y_train, y_test)
    
#import h5py
#from keras.models import load_model
#reconstructed_model = load_model("trainedModel.h5")

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

#------------- MODEL DEVELOP ----------------#
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

model = Sequential()
model.add(LSTM(units = n_past))
model.add(Dropout(.25))
model.add(Dense(1))
    
model.compile(optimizer='adam', loss = 'mean_squared_error')
model.fit(X_train, y_train, epochs = 10, batch_size=10)
model.summary()
y_predictions = model.predict(X_test)
msl.mseCalculator(y_predictions, y_test)


from sklearn.metrics import r2_score
print(' R2 degeri:',r2_score(y_test,y_predictions))


real_close = mdl.inverseScaler(model_data, y_test)
lstm_predictions = mdl.inverseScaler(model_data, y_predictions)

trend_lstm = msl.trendCalculator(y_predictions)
trend_real = msl.trendCalculator(y_test)

#msl.metricsCalculator(trend_lstm[6:], trend_real[:len(trend_real) - 6])
msl.metricsCalculator(trend_lstm[1:], trend_real[:-1])


import PredictionGraphLibrary
PredictionGraphLibrary.printGraph(lstm_predictions, real_close)


#import pickle 
#importModel = pickle.load(open("monsterModel.kayit", 'rb'))
#
#monsterTahminler = importModel.predict(X_test)


##
#model = Sequential()
#model.add(LSTM(units = n_past))
#model.add(Dropout(0.25))
#model.add(Dense(1))
#
#model.compile(optimizer='adam', loss = 'binary_crossentropy')
#model.fit(X_train, y_label_train, epochs = 5, batch_size=128)
#model.summary()
#
#y_predictions = model.predict(X_test)
#
#def yLabelPredictions(y_predictions):
#    from statistics import median
#    threshold = median(y_predictions)
#    y_label_predictions = list()
#    for prediction in y_predictions:
#        if prediction >= threshold:
#            y_label_predictions.append(-1)
#        else:
#            y_label_predictions.append(1)
#            
#    return y_label_predictions
#
#y_label_predictions = yLabelPredictions(y_predictions)
#
#msl.metricsCalculator(y_label_predictions, y_label_test)

