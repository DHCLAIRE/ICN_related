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

def LISTblankEraser(rawLIST):
    newrawLIST = []
    for row in rawLIST:
        if len(row) == 0:
            rawLIST.pop(rawLIST.index(row))
        else:
            pass
    newrawLIST = rawLIST
    print(len(newrawLIST))
    return newrawLIST

def Mean(resultLIST, i, typeSTR = None):
    contentLIST = []
    for row in resultLIST:
        if type(row) == list:
            rawLIST = row
            contentLIST.append(float(rawLIST[i]))
        else:
            rawLIST = row.split(",")
            contentLIST.append(float(rawLIST[i]))
    print("Raw data:", contentLIST)
    old_count = len(contentLIST)
    print(old_count)

    for RT_Int in contentLIST:
        if 0. in contentLIST:
            contentLIST.remove(0.0)
        else:
            pass
    print("Exclude 0.0 data:", contentLIST)
    new_count = len(contentLIST)
    print(new_count)
    
    exclude_countINT = old_count - new_count
    PLDTmean_subFLOAT = round(np.mean(np.array(contentLIST)),3) #ouput: H pwRT Mean : 783.167
    MeanDICT = {"{} count".format(typeSTR):len(contentLIST),"{} Mean".format(typeSTR):PLDTmean_subFLOAT, "Exclude 0.0 count": exclude_countINT}
    
    return MeanDICT


def correctness(resultLIST, typeSTR = None):
    correctnessLIST = []
    count_True = 0 
    count_False = 0
    count_NA = 0
    
    for row in resultLIST:
        #rawLIST = ListDetector(row)
        if type(row) == list:
            rawLIST = row
        else:
            rawLIST = row.split(",")
            
        if rawLIST[6] == "['True']":
            count_True += 1
            correctBOOL = 1
        elif rawLIST[6] == "['False']":
            count_False += 1
            correctBOOL = 0
        else:
            count_NA += 1
            
    total_correctFLOAT = round(count_True/(count_True + count_False)*100,2)
    correctnessDICT = {"{} Correctness".format(typeSTR): total_correctFLOAT, "{} True:".format(typeSTR): count_True, "{} False:".format(typeSTR): count_False, "{} N/A:".format(typeSTR): count_NA}
    #correctnessLIST = [count_True, count_False, count_NA, total_correctFLOAT]
    
    return correctnessDICT  #correctnessLIST,   ###count_True, count_False, count_NA, total_correctFLOAT



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
        
        #print(sub_num)
        
        targetPseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])
        High_CDpwLIST.extend(pseudoDICT["High_CD condition pseudowords_3"])
        Low_CDpwLIST.extend(pseudoDICT["Low_CD condition pseudowords_3"])
        
        print(sub_num, "Target pw : ", targetPseudoLIST)
        print(sub_num, "High-CD pw : ", High_CDpwLIST)
        print(sub_num, "Low-CD pw : ", Low_CDpwLIST) # output: 003 Low-CD pw :  ['vaesow', 'payliy', 'paenliy']
        
    #pass
    # raw data
    rawLIST = []
    H_CD_rawLIST = []
    L_CD_rawLIST = []
    
    ## PER PERSON ##
    # Mean
    H_pwRT_DICT = {}
    L_pwRT_DICT = {}
    # Correctness (True & False)
    PLDT_correct_subLIST = []
    H_PLDT_correct_subLIST = []
    L_PLDT_correct_subLIST = []
    # Self_rating
    rating_Mean_LIST = []
    H_CD_ratingMean_subLIST = []
    L_CD_ratingMean_subLIST = []
    
    """
    ## WHOLE GROUP ##
    # Mean
    H_PLDTmean_allLIST = []
    L_PLDTmean_allLIST = []
    # SD
    H_PLDTsd_allLIST = []
    L_PLDTsd_allLIST = []
    """
    
    # For LDT results calculation  >> should I add True/False calculation???
    with open (result_data_path + "003_LDT_results.csv", "r", encoding = "utf-8") as csvfile:
        resultLIST = csvfile.read().split("\n")
        print(resultLIST)
        print()
        print(len(resultLIST))
        resultLIST.pop(0)   # exclude the headers
        print(len(resultLIST))
        
        # exclude the blank row
        resultLIST = LISTblankEraser(resultLIST)

    # Finding the wanted H & L CD response, and then calculate the Mean of H & L pwRT
    for row in resultLIST:
        rawLIST = row.split(",")
        if rawLIST[2] in High_CDpwLIST:
            #print("High CD pw: ", rawLIST)
            H_CD_rawLIST.append(rawLIST)
        elif rawLIST[2] in Low_CDpwLIST:
            #print("Low CD pw: ", rawLIST)
            L_CD_rawLIST.append(rawLIST)
        else:
            pass
    print(H_CD_rawLIST)
    print(len(H_CD_rawLIST))
    print(L_CD_rawLIST)
    print(len(L_CD_rawLIST))
    
    # Calculate the RT Mean of the H & L PLDT
    H_pwRT_DICT = Mean(H_CD_rawLIST,5 , "High-CD RT")  #{'High-CD RT count': 30, 'High-CD RT Mean': 783.167, 'Exclude 0.0 count': 0}
    L_pwRT_DICT = Mean(L_CD_rawLIST,5 , "Low-CD RT")
    print(H_pwRT_DICT)
    print(L_pwRT_DICT)

    # Calculate the Correctness of all, and H & L PLDT, there's three in total
    PLDT_correct_subLIST = correctness(resultLIST, "PLDT-total")
    H_PLDT_correct_subLIST = correctness(H_CD_rawLIST, "H-CD PLDT")
    L_PLDT_correct_subLIST = correctness(L_CD_rawLIST, "L-CD PLDT")  # ouput = ([27, 2, 1, 93.1], {'Correct :': 27, 'False :': 2, 'N/A :': 1, 'Correctness': 93.1}) # type = <class 'tuple'>
    
    print(PLDT_correct_subLIST)
    print(H_PLDT_correct_subLIST)
    print(L_PLDT_correct_subLIST)
    print(type(H_PLDTmean_subLIST))
    
    
    
    
    
    
    """
    # Self_rating section
    readingLIST = []
    
    with open (result_data_path + "003_Reading_task.csv", "r", encoding= 'unicode_escape') as csvfile_reading:  #, "r", encoding = "utf-8")
        readingLIST = csvfile_reading.read().split("\n")
        #pprint(readingLIST)
        print(type(readingLIST))
        print(len(readingLIST))
        readingLIST.pop(0)   # exclude the headers
        print(len(readingLIST))
        
        # exclude the blank row
        readingLIST = LISTblankEraser(readingLIST)
        print(len(readingLIST))
        
    ratingLIST = []
    
    #pprint(readingLIST)
    
    for row in readingLIST:
        rawLIST = row.split(",")
        rating_Mean = Mean(4, rawLIST, "Self-Rating")
    pprint(rating_Mean)
    """
    """
    # Calculate the Self_rating mean of 30 short texts
    for row in readingLIST:
        rawLIST = row.split(",")
        print(rawLIST)
        print(type(rawLIST))
        ratingLIST.append(float(rawLIST[4]))
    print(ratingLIST)
    
    
    rating_meanFLOAT = round(np.mean(np.array(ratingLIST)),2)
    print(rating_meanFLOAT)
    print(type(rating_meanFLOAT))
    
    H_ratingLIST = []
    L_ratingLIST = []
    """
    """
    #003 High-CD pw :  ['aegliy', 'baydiy', 'chaeviy']
    #003 Low-CD pw :  ['vaesow', 'payliy', 'paenliy']
    """
    """
    # Calculate the Self_rating mean of H-CD & L-CD short texts
    for row in readingLIST:
        rawLIST = row.split(",")
        for Hpw in High_CDpwLIST:
            if Hpw in rawLIST[5]:
                print("H-CD stim: ", rawLIST[5])
            else:
                pass
        for Lpw in Low_CDpwLIST:
            if Lpw in rawLIST[5]:
                print("L-CD stim: ", rawLIST[5])
            else:
                pass
        
        #if Low_CDpwLIST in rawLIST[5]:
            #print("L-CD stim: ", rawLIST)
        #else:
            #print("ERROR!!")
        
        #ratingLIST.append(float(rawLIST[4]))
    #print(ratingLIST)
    
    #rating_meanFLOAT = round(np.mean(np.array(ratingLIST)),2)
    #print(rating_meanFLOAT)
    #print(type(rating_meanFLOAT))
    """