import numpy as np


class Metrics():
    def __init__(self, predictions, testData):
        self.__predictions = np.array(predictions)
        self.__testData = np.array(testData)

    def calculate_mse(self):
        return (np.sqrt(sum((self.__predictions - self.__testData)**2)))

    def calculateMetrics(self):
        tp = []
        fp = []
        fn = []
        tn = []
        
        for i in range(0, len(self.__predictions)):
            if (self.__predictions[i] == 1 and self.__testData[i] == 1):
                tp.append(1)
            elif (self.__predictions[i] == -1 and self.__testData[i] == 1):
                fp.append(1)
            elif (self.__predictions[i] == 1 and self.__testData[i] == -1):
                fn.append(1)
            elif (self.__predictions[i] == -1 and self.__testData[i] == -1):
                tn.append(1)
                
        acc = (len(tp) + len(tn)) / len(self.__predictions)
        precision = len(tp) / (len(tp) + len(fp))
        recall = len(tp) / (len(fn) + len(tp))
        f1_score = (2*precision * recall) / (precision + recall)
        
        print('accuracy:', acc)
        print('\nprecision:', precision)
        print('\nrecall:', recall)
        print('\nf1 score:', f1_score)

    def labelClasses(self):
        classes = []
        for out in self.__predictions:
            if out > self.__predictions.mean():
                classes.append(-1)
            else:
                classes.append(+1)
                
        return classes

    def accuracyCalculator(self):
        acc = []
        for i in range(0,len(self.__predictions)):
            if self.__predictions[i] != self.__testData[i]:
                acc.append(0)
            else:
                acc.append(1)
                
        print((sum(acc) / len(acc)))
            
    
    def trendCalculator(self):
        trend = []
        for i in range(0, len(self.__predictions) - 1):
            if self.__predictions[i+1] - self.__predictions[i] >= 0:
                trend.append(1)
            else:
                trend.append(-1)
                
        return trend

    def trendCalculatorBias(self):
        trend = []
        for i in range(0, len(self.__predictions) - 1):
            if self.__predictions[i+1] - self.__predictions[i] >= 0.25:
                trend.append(1)
            else:
                trend.append(-1)
                
        return trend


