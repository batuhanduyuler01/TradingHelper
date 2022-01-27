#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
date: 10-07-2021

@author: batuhanduyuler
"""
import numpy as np

def mseCalculator(y_tahmin, y_gercek):
    
    print(np.sqrt(sum((y_tahmin - y_gercek)**2) ))
    

def metricsCalculator(prediction, real):
    tp = []
    fp = []
    fn = []
    tn = []
    
    for i in range(0, len(prediction)):
        if (prediction[i] == 1 and real[i] == 1):
            tp.append(1)
        elif (prediction[i] == -1 and real[i] == 1):
            fp.append(1)
        elif (prediction[i] == 1 and real[i] == -1):
            fn.append(1)
        elif (prediction[i] == -1 and real[i] == -1):
            tn.append(1)
            
    acc = (len(tp) + len(tn)) / len(prediction)
    precision = len(tp) / (len(tp) + len(fp))
    recall = len(tp) / (len(fn) + len(tp))
    f1_score = (2*precision * recall) / (precision + recall)
    
    print('accuracy:', acc)
    print('\nprecision:', precision)
    print('\nrecall:', recall)
    print('\nf1 score:', f1_score)
    
    
def classLabels(prediction):
    classes = []
    for out in prediction:
        if out > prediction.mean():
            classes.append(-1)
        else:
            classes.append(+1)
            
    return classes

def accuracyCalculator(prediction, real):
    acc = []
    for i in range(0,len(prediction)):
        if prediction[i] != real[i]:
            acc.append(0)
        else:
            acc.append(1)
            
    print((sum(acc) / len(acc)))
            
    
def trendCalculator(prediction):
    trend = []
    for i in range(0, len(prediction) - 1):
        if prediction[i+1] - prediction[i] >= 0:
            trend.append(1)
        else:
            trend.append(-1)
            
    return trend

def trendCalculatorBias(prediction):
    trend = []
    for i in range(0, len(prediction) - 1):
        if prediction[i+1] - prediction[i] >= 0.25:
            trend.append(1)
        else:
            trend.append(-1)
            
    return trend
