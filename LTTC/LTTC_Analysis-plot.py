#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from pprint import pprint
import csv
import json
import random
from random import sample
import numpy as np
from datetime import datetime,date
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import statistics

def LISTblankEraser(rawLIST):
    '''
    Remove the blank item inside the list
    '''
    newrawLIST = []
    for row in rawLIST:
        if len(row) == 0:
            rawLIST.pop(rawLIST.index(row))
        else:
            pass
    newrawLIST = rawLIST
    return newrawLIST

if __name__ == "__main__":
    
    result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"
    
    resultLIST = []
    n_resultLIST = []
    
    # RT
    H_rawRT_LIST = []
    L_rawRT_LIST = []
    H_finalRT_LIST = []
    L_finalRT_LIST = []
    
    # Correctness
    ALL_Correctness_LIST = []
    H_raw_Correctness_LIST = []
    L_raw_Correctness_LIST = []
    H_final_Correctness_LIST = []
    L_final_Correctness_LIST = []
    
    # Self-rating 
    Self_rating_Mean_LIST = []
    H_Self_rating_Mean_LIST = []
    L_Self_rating_Mean_LIST = []
    
    # Self-reading
    Self_readingT_minMean_LIST = []
    H_Self_readingT_minMean_LIST = []
    L_Self_readingT_minMean_LIST = []
    
    
    with open (result_data_path + "PLDT_analyzed_results.csv", "r", encoding = "utf-8") as csvfile:
        """
        resultLIST = csvfile.read().split("\n")
        resultLIST.pop(0)
        resultLIST = LISTblankEraser(resultLIST)
        print(len(resultLIST))
        """
        
        data = pd.read_csv(csvfile, index_col=0)
        data.plot.scatter(x = "(%)ALL_Correctness", y = "(ms)H_raw_RTMean", alpha = 0.5)
        data.plot()
        
    """
    for row in resultLIST:
        rawLIST = row.split(",")
        rawLIST = np.array(rawLIST)
        n_resultLIST.append(rawLIST)
        
    print(n_resultLIST)
    print(type(n_resultLIST))
        # Setting the wanted X & Y axis
    
    data = pd.DataFrame(np.array(n_resultLIST), columns=['Sub_id',
                                                       '(ms)H_raw_RTMean',
                                                       '(ms)H_final_RTMean',
                                                       '(ms)L_raw_RTMean',
                                                       '(ALL_Correctnessms)L_final_RTMean',
                                                       '(%)ALL_Correctness',
                                                       '(%)H_raw_Correctness',
                                                       '(%)H_final_Correctness',
                                                       '(%)L_raw_Correctness',
                                                       '(%)L_final_Correctness',
                                                       'Self_rating_Mean',
                                                       'H_Self_rating_Mean',
                                                       'L_Self_rating_Mean',
                                                       '(ms)Self_readingT_msMean',
                                                       '(ms)H_Self_readingT_msMean',
                                                       '(ms)L_Self_readingT_msMean',
                                                       '(min)Self_readingT_minMean',
                                                       '(min)H_Self_readingT_minMean',
                                                       '(min)L_Self_readingT_minMean'])
    """

    #plt.plot(data)
    #plot(x = '(%)ALL_Correctness', y = )
    
    """
    for row in resultLIST:
            rawLIST = row.split(",")
            
            ALL_Correctness_LIST.append(rawLIST[5])   # correctness
            H_rawRT_LIST.append(rawLIST[1])   # RT(High & Low)
            L_rawRT_LIST.append(rawLIST[3])
        
        
        # Plotting section
        
        # ploting the RT & Correctness
        plt_1.scatter(ALL_Correctness_LIST, H_rawRT_LIST)
        plt_2.scatter(ALL_Correctness_LIST, L_rawRT_LIST)
        plt.show()
        """ 
