#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
date: 09-07-2021

@author: batuhanduyuler
"""

import pandas as pd
import numpy as np


def minmaxScaler(dataframe):
    
    df = dataframe.copy()
    column_list = df.columns
    yasaklilar = ['Date', 'Label', 'Previous_Label']
    
    for i in range(len(df.columns)):
        if column_list[i] in yasaklilar: 
            pass
        else:
            temp_maksimum = max(df[column_list[i]])
            temp_minimum = min(df[column_list[i]])
            temp_denominator = (temp_maksimum - temp_minimum)
            
            df[column_list[i]] = (df[column_list[i]] - temp_minimum) / temp_denominator 
    
    return df


def train_test_split(dataframe, train_size = 0.8):
    
    df = dataframe.copy()
    end = round(len(df) * train_size)
    train = df[:end]
    test = df[end:]
    
    train = train.reset_index(drop = True)
    test = test.reset_index(drop = True)
    
    return train, test   

def splitData(data, n_past, n_future):
    #n_past -> kaç tane geçmiş gün olduğu
    #n_future -> kaç tane gelecek gün tahmin etmek istediğimiz
    
    yasaklilar = ['Date', 'Next_Close']
    #yasaklilar = ['Next_Close']
    futures = data.columns.to_list()
    for future in futures:
        if future in yasaklilar:
            data = data.drop([future], axis = 1)
            
    X, y = [], []
    y_label = []
    
    
    
    index_no = data.columns.get_loc("Close")
    
    data = data.values
    n = len(data)
    for window_start in range(0,n):
        past_end = window_start + n_past
        future_end = past_end + n_future
        
        if future_end > n:
            break
            
        past, future = data[window_start:past_end, :-1], data[past_end:future_end, index_no]
        X.append(past)
        y.append(future)
        y_label.append(data[past_end - 1, -1])
        
    return np.array(X), np.array(y), np.array(y_label).reshape(-1,1)



    
    
def reshapeData_X(X_train, X_test):
    
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], X_train.shape[2] )) 
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], X_train.shape[2]))
    
    return X_train, X_test

def reshapeData_y(y_train, y_test):
    
    y_train = y_train.reshape((y_train.shape[0], y_train.shape[1]))
    y_test = y_test.reshape((y_test.shape[0], y_test.shape[1]))
    return y_train, y_test



def inverseScaler(old_data, new_data):
    temp_maksimum = max(old_data["Close"])
    temp_minimum = min(old_data["Close"])
    temp_denominator = (temp_maksimum - temp_minimum)
    
    return np.round(new_data * (temp_denominator) + temp_minimum, 5)




    

    
    
def futureSplitData(data, n_past, n_future, dayForward = 1):
    #n_past -> kaç tane geçmiş gün olduğu
    #n_future -> kaç tane gelecek gün tahmin etmek istediğimiz
    
    yasaklilar = ['Date', 'Next_Close']
    #yasaklilar = ['Next_Close']
    futures = data.columns.to_list()
    for future in futures:
        if future in yasaklilar:
            data = data.drop([future], axis = 1)
            
    X, y = [], []
    ####Bu kısım Close parametresini datadan çıkartmak için###
    temp_df = data.drop(["Close"], axis = 1)
    
    
    
    index_no = data.columns.get_loc("Close")
    
    data = data.values
    temp = temp_df.values
    n = len(data)
    for window_start in range(0,n):
        past_end = window_start + n_past
        future_end = past_end + n_future + dayForward
        
        if future_end > n:
            break
            
        past, future = temp[window_start:past_end, :-1], data[past_end+dayForward:future_end, index_no]
        X.append(past)
        y.append(future)
        
    return np.array(X), np.array(y)
    
    
    
    
    
    
    
    
    
    
    