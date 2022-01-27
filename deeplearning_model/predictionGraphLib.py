#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
date: 15-07-2021

@author: batuhanduyuler
"""

import matplotlib.pyplot as plt

def printGraph(prediction, real):
    
    cerceve = plt.figure(figsize=(10,5))
    plt.plot(real)
    plt.plot(prediction)
    cerceve.suptitle('Long Short Term Memory \n')
    plt.ylabel('Closing Price (TL)')
    plt.xlabel('Days')
    plt.legend(['Actual', 'Prediction'])
    plt.show()

