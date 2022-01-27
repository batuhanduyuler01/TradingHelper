#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
date  : 09-07-2021
@author: batuhanduyuler
"""
import pandas as pd
import numpy as np

def tarih_ayarlama(dataframe, tarih):
    df = dataframe.copy()
    if tarih > max(dataframe["Date"]):
        raise AssertionError()
        
    else:
        #datasette, bu tarihe eşit ve sonraki tarihleri tüm kolonlarla al
        df = df[df.Date >= tarih]
        #verisetinde indexler var [0...N] şeklinde
        #bazı satırları aldığımız için indexle değişir. Tekrar [0..N] haline getiriyoruz.
        df = df.reset_index(drop = True) 
    
    return df



def volumeCheck(dataframe):
    
    df = dataframe.copy()
    hacimDegisikligi = 0
    
    for indx, row in df.iterrows():
        
        dummy_condition = False
        volume_condition = False
        
        if row["Volume"] == 0:
            volume_condition = True
        if row["Open"] == row["Close"] == row["High"] == row["Low"]:
            dummy_condition = True
        
        if (volume_condition == True and dummy_condition == True):
            df.drop(axis = 0, index = indx, inplace = True)
        elif (dummy_condition == False and volume_condition == True):
            
            hacimDegisikligi += 1
            if (indx != 0 and indx != 1):
                temp_change = (df["Volume"][indx-2:indx+2]).mean()
                df.at[indx, "Volume"] = temp_change
            else:
                temp_change = (df["Volume"][indx:indx+4]).mean()
                df.at[indx, "Volume"] = temp_change
        
    new_df = df.reset_index(drop=True)
    return new_df


def obtainLabels(dataframe):
    df = dataframe.copy()
    
    labels = []
    n = len(df)
    
    for i in range(0,n-1):
        temp_trend = np.sign(df["Close"][i+1] - df["Close"][i])
        if temp_trend == 0:
            temp_trend = 1
            
        labels.append(temp_trend)
        
    new_df = df.drop(index = df.index[-1])    
    new_df.insert(new_df.shape[1], "Label", labels, True)
    
    return new_df


def obtainPreviousLabel(dataframe):
    df = dataframe.copy()
    
    previous_labels = []
    n = len(df)
    
    for i in range(0,n-1):
        prev_trend = np.sign(df["Close"][i+1] - df["Close"][i])
        if prev_trend == 0:
            prev_trend = 1
            
        previous_labels.append(prev_trend)
        
    new_df = df.drop(index = 0)
    new_df = new_df.reset_index(drop = True)
    
    new_df.insert(new_df.shape[1] - 1, "Previous_Label", previous_labels, True)
    return new_df
