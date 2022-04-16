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
    
    with open (result_data_path + "001_LDT_results.csv", "r", encoding = "utf-8") as csvfile:
        resultLIST = csvfile.read().split("\n")
        #print(resultLIST)
        #print(len(resultLIST))
        
        for row in resultLIST:
            tmpLIST = row.split(",")
            if tmpLIST[2] in High_CDpwLIST:
                #print("There's the High-CD result!")
                High_CDRT_LIST.append(tmpLIST[5])
            elif tmpLIST[2] in Low_CDpwLIST:
                #print("There's the Low-CD result!")
                Low_CDRT_LIST.append(tmpLIST[5])
            else:
                pass
                #print("N/A")
                
        print("High-CD RT LIST = ", High_CDRT_LIST)
        print(len(High_CDRT_LIST))
        print("Low-CD RT LIST = ", Low_CDRT_LIST)
        print(len(Low_CDRT_LIST))
        
        for High_RT in High_CDRT_LIST:
            High_RTInt = int(High_RT)
            Start_HighRT = index(High_RTInt, 1)
            High_RTInt += in
            print(High_RTInt)
            print(type(High_RTInt))