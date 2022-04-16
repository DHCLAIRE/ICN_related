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
    
    
    # key in number for notifying which subject it is
    sub_id = str(input("Subject: "))
    
    #剩把pseudoDICT的值叫出來
    pseudoLIST = []
    targetPseudoLIST = []
    #controlPseudoLIST = []
    #words_high_CD_setLIST = []
    #words_low_CD_setLIST = []
    High_CDpwLIST = []
    Low_CDpwLIST = []
    
    
    DICT_name = sub_id + '_pseudowordsDICT.json'
    Dsave_path = result_data_path + DICT_name
    
    with open (Dsave_path, "r", encoding = "utf-8") as jfile:
        pseudoDICT = json.load(jfile)
        pprint(pseudoDICT)
        
        targetPseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])
        High_CDpwLIST.extend(pseudoDICT["High_CD condition pseudowords_3"])
        Low_CDpwLIST.extend(pseudoDICT["Low_CD condition pseudowords_3"])
        
        print(targetPseudoLIST)
        print(High_CDpwLIST)
        print(Low_CDpwLIST)
        
    #pass
    
    
    """
    with open (result_data_path + "001_LDT_results.csv", "r", encoding = "utf-8") as csvfile:
        resultLIST = csvfile.read().split("\n")
        #print(resultLIST)
        #print(len(resultLIST))
        
        for row in resultLIST:
            tmpLIST = row.split(",")
            print(tmpLIST)
            print(tmpLIST[2])
            print(type(tmpLIST[2]))
            for target_pw in 
            if tmpLIST[2] == 
            """


