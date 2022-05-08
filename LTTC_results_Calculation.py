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
from collections import Counter

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

def total_elements(list):
    count = 0
    for element in list:
        count += 1
    return count



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
    
    sub_num = "003"
    
    with open (result_data_path + "003_pseudowordsDICT.json", "r", encoding = "utf-8") as jfile:
        pseudoDICT = json.load(jfile)
        pprint(pseudoDICT)
        
        print(sub_num)
        
        targetPseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])
        High_CDpwLIST.extend(pseudoDICT["High_CD condition pseudowords_3"])
        Low_CDpwLIST.extend(pseudoDICT["Low_CD condition pseudowords_3"])
        
        print(sub_num, "Target pw : ", targetPseudoLIST)
        print(sub_num, "High-CD pw : ", High_CDpwLIST)
        print(sub_num, "Low-CD pw : ", Low_CDpwLIST)
        
    #pass
    # raw data
    rawLIST = []
    H_CD_rawLIST = []
    L_CD_rawLIST = []
    H_rtLIST = []
    L_rtLIST = []
        
    ## PER PERSON ##
    # Mean
    H_PLDTmean_subLIST = []
    L_PLDTmean_subLIST = []
    # Correctness (True & False)
    PLDT_correct_subLIST = []
    H_PLDT_correct_subLIST = []
    L_PLDT_correct_subLIST = []
    # Self_rating
    rating_Mean_LIST = []
    H_CD_ratingMean_subLIST = []
    L_CD_ratingMean_subLIST = []
    
    
    ## WHOLE GROUP ##
    # Mean
    H_PLDTmean_allLIST = []
    L_PLDTmean_allLIST = []
    # SD
    H_PLDTsd_allLIST = []
    L_PLDTsd_allLIST = []
    
    
    # For LDT results calculation  >> should I add True/False calculation???
    with open (result_data_path + "003_LDT_results.csv", "r", encoding = "utf-8") as csvfile:
        resultLIST = csvfile.read().split("\n")
        print(len(resultLIST))
        resultLIST.pop(0)   # exclude the headers
        print(len(resultLIST))
        
        # exclude the blank row
    for row in resultLIST:
        if len(row) == 0:
            resultLIST.pop(resultLIST.index(row))
        else:
            pass
    print(len(resultLIST))
        
    # Finding the wanted H & L CD response, and then calculate the Mean of H & L pwRT
    for row in resultLIST:
        rawLIST = row.split(",")
        if rawLIST[2] in High_CDpwLIST:
            print("High CD pw: ", rawLIST)
            H_CD_rawLIST.append(rawLIST)
        elif rawLIST[2] in Low_CDpwLIST:
            print("Low CD pw: ", rawLIST)
            L_CD_rawLIST.append(rawLIST)
        else:
            pass
    print(H_CD_rawLIST)
    print(len(H_CD_rawLIST))
    print(L_CD_rawLIST)
    print(len(L_CD_rawLIST))
        
    for row in H_CD_rawLIST:
        H_rtLIST.append(float(row[5]))
        if 0. in H_rtLIST:
            H_rtLIST.remove(0.0)
        else:
            pass
    #print(H_rtLIST)
    print(len(H_rtLIST))
    H_PLDTmean_subFLOAT = round(np.mean(np.array(H_rtLIST)),3)
    print("H pwRT Mean :", H_PLDTmean_subFLOAT)
    
    for row in L_CD_rawLIST:
        L_rtLIST.append(float(row[5]))
        if 0. in L_rtLIST:
            L_rtLIST.remove(0.0)
        else:
            pass
    #print(L_rtLIST)
    print(len(L_rtLIST))
    L_PLDTmean_subFLOAT = round(np.mean(np.array(L_rtLIST)),3)
    print("L pwRT Mean :", L_PLDTmean_subFLOAT)
    
    
    # Calculate the Correctness of all, and H & L PLDT, there's three in total
    
    # count the total correctness
    count_True = 0 #dict()
    count_False = 0
    count_NA = 0
    for row in resultLIST:
        rawLIST = row.split(",")
        if rawLIST[6] == "['True']":
            count_True += 1
            correctBOOL = 1
        elif rawLIST[6] == "['False']":
            count_False += 1
            correctBOOL = 0
        else:
            count_NA += 1
            
    print(count_True)
    print(count_False)
    print(count_NA)
    # Total correctness section
    total_correctFLOAT = round(count_True/(count_True + count_False)*100,2)
    print(total_correctFLOAT)
    #print(rawLIST)
    