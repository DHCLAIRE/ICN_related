#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# for stimuli
from pprint import pprint
import csv
import json
import random
from random import sample
import numpy as np
from datetime import datetime,date
import pandas as pd

"""
# What should we calculate??
PLDT_High-CDRT_Mean
Low-CDRT_Mean
PLDT-Correctness
SelfPRT_Mean

# Should this be calculate as well??
  >> Calculate the mean of RT in each level of rating >>??  But it would be blank if the subject left our some rating...
SelfPRT_Rate1_count
SelfPRT_Rate2_count
SelfPRT_Rate3_count
SelfPRT_Rate4_count
SelfPRT_Rate5_count
SelfPRT_Rate6_count
SelfPRT_Rate7_count
"""

"""
np.mean => only accept np.array
"""
def Sum(RT_LIST):
    '''
    將LIST裡的值累加起來
    '''
    count = 0
    for i in RT_LIST:
        count+= int(i)
    return count

def RT_Mean(RT_LIST):
    '''
    取得LIST裡所有值的平均值，並取到小數點第四位
    '''
    RT_MeanFloat = round(Sum(RT_LIST)/len(RT_LIST), 4)
    return RT_MeanFloat



if __name__ == "__main__":
    
    # Setting up the data_path
    result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"
    
    resultLIST = []
    tmpLIST = []
    
    #剩把pseudoDICT的值叫出來
    pseudoLIST = []
    targetPseudoLIST = []
    High_CDpwLIST = []
    Low_CDpwLIST = []
    
    High_CDRT_LIST = []
    Low_CDRT_LIST = []
    
    
    with open (result_data_path + "001_pseudowordsDICT.json", "r", encoding = "utf-8") as jfile:
        pseudoDICT = json.load(jfile)
        pprint(pseudoDICT)
        
        targetPseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])
        High_CDpwLIST.extend(pseudoDICT["High_CD condition pseudowords_3"])
        Low_CDpwLIST.extend(pseudoDICT["Low_CD condition pseudowords_3"])
        
        print("Target pw : ", targetPseudoLIST)
        print("High-CD pw : ", High_CDpwLIST)
        print("Low-CD pw : ", Low_CDpwLIST)
        
    #pass
    
    # For LDT results calculation  >> should I add True/False calculation???
    with open (result_data_path + "001_LDT_results.csv", "r", encoding = "utf-8") as csvfile:
        resultLIST = csvfile.read().split("\n")
        #print(resultLIST)
        #print(len(resultLIST))
        
        for row in resultLIST:
            tmpLIST = row.split(",")
            if tmpLIST[2] in High_CDpwLIST:
                High_CDRT_LIST.append(tmpLIST[5])
            elif tmpLIST[2] in Low_CDpwLIST:
                Low_CDRT_LIST.append(tmpLIST[5])
            else:
                pass
            
            print(tmpLIST)
                
        print("High-CD RT LIST = ", High_CDRT_LIST)
        print(len(High_CDRT_LIST))
        print("Low-CD RT LIST = ", Low_CDRT_LIST)
        print(len(Low_CDRT_LIST))
        
        for HighRT_STR in High_CDRT_LIST:
            if "0" == HighRT_STR:
                High_CDRT_LIST.remove(HighRT_STR)
                final_High_RT_LIST = High_CDRT_LIST
            if len(HighRT_STR) == 1 and HighRT_STR != "0":
                High_CDRT_LIST.remove(HighRT_STR)
                final_High_RT_LIST = High_CDRT_LIST
            else:
                final_High_RT_LIST = High_CDRT_LIST
        print(final_High_RT_LIST)
        print(len(final_High_RT_LIST))
        
        
        for LowRT_STR in Low_CDRT_LIST:
            if "0" == LowRT_STR:
                Low_CDRT_LIST.remove(LowRT_STR)
                final_Low_RT_LIST = Low_CDRT_LIST
            if len(LowRT_STR) == 1 and LowRT_STR != "0":
                Low_CDRT_LIST.remove(LowRT_STR)
                final_Low_RT_LIST = Low_CDRT_LIST
            else:
                final_Low_RT_LIST = Low_CDRT_LIST
        print(final_Low_RT_LIST)
        print(len(final_Low_RT_LIST))
        
        
        High_Mean = RT_Mean(final_High_RT_LIST)  #round(Sum(final_High_RT_LIST)/len(final_High_RT_LIST), 4)
        Low_Mean = RT_Mean(final_Low_RT_LIST)
        
        print(High_Mean)
        print(type(High_Mean))
        print(Low_Mean)
        print(type(Low_Mean))
        
        
    # For SelfPRT_Mean
    with