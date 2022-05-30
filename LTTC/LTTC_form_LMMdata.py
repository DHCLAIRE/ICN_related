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

def get_List(resultLIST, i):
    '''
    Extract the wanted data from the raw data LIST
    '''
    contentLIST = []
    for row in resultLIST:
        if type(row) == list:
            rawLIST = row
            contentLIST.append(float(rawLIST[i]))
        else:
            rawLIST = row.split(",")
            contentLIST.append(float(rawLIST[i]))
    return contentLIST

def remove_value(contentLIST, value):
    '''
    Exclude the missing_value
    '''
    for k in contentLIST:
        if float(value) in contentLIST:
            contentLIST.remove(float(value))
        else:
            pass
    return contentLIST

def get_NA_count(A_LIST, countINT):
    '''
    Get the excluded N/A count
    '''
    raw_count = len(A_LIST)
    if raw_count != countINT:
        exclude_countINT = countINT - raw_count
    else:
        exclude_countINT = 0
        
    return exclude_countINT

def Mean(resultLIST):
    '''
    Get the mean of the target data LIST
    '''
    meanFLOAT = round(np.mean(np.array(resultLIST)), 3)
    return meanFLOAT

def STD(resultLIST, df):
    '''
    Get the STD of the target data LIST
    '''
    stdFLOAT = round(np.std(np.array(resultLIST), ddof = df),3)
    return stdFLOAT

def ms_to_min(INT):
    '''
    Turn the miliseconds into minutes
    '''
    minFLOAT = round(INT/1000/60, 3)
    return minFLOAT

"""
def Mean(resultLIST, item_index, missing_value, total_count, typeSTR = None):
    '''
    Get the mean of the cleaned data list
    '''
    contentLIST = get_List(resultLIST, item_index)
    contentLIST = remove_value(contentLIST, missing_value)
    NA_count = get_NA_count(contentLIST, total_count)
    meanFLOAT = round(np.mean(np.array(contentLIST)), 3) #ouput: H pwRT Mean : 783.167
    MeanDICT = {"{} count".format(typeSTR):len(contentLIST),"{} Mean".format(typeSTR):meanFLOAT , "Exclude 0.0 count": NA_count}
    
    return MeanDICT

def STD(resultLIST, i, df, typeSTR = None):

    PLDTstd_subFLOAT = round(np.std(np.array(contentLIST), ddof = df),3) #ouput: H pwRT Mean : 783.167
    StdDICT = {"{} count".format(typeSTR):len(contentLIST),"{} STD".format(typeSTR):PLDTstd_subFLOAT, "Exclude 0.0 count": exclude_countINT}
    
    return StdDICT
"""

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

    # sub_num/ condition(New word/ H_CD / L_CD) / trials / items(pseudowords_代號或pw本身) / times (出現的次數) / ACC (True_1; False_0) / RT 
    
    
if __name__ == "__main__":
    result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"
    
    for z in range(1):
        # raw data
        resultLIST = []
        rawLIST = []
        
        # wanted columnLIST
        sub_idLIST = []
        conditionLIST = []
        trialLIST = []
        itemLIST = []
        appearanceLIST = []
        TandF_LIST = []
        RTLIST = []
        
        sub_num = "0{0:02d}".format(z+7)
        # For LDT results calculation  >> should I add True/False calculation???
        with open (result_data_path + "{}_LDT_results.csv".format(sub_num), "r", encoding = "utf-8") as csvfile:
            resultLIST = csvfile.read().split("\n")
            #pprint(resultLIST)
            #print(len(resultLIST))
            resultLIST.pop(0)   # exclude the headers
            #print(len(resultLIST))
        
            # exclude the blank row
            resultLIST = LISTblankEraser(resultLIST)
        
        trials_count = 0
        
        for row in resultLIST:
            rawLIST = row.split(",")
            print(rawLIST)   # ['007', '2022-04-19', 'chaeviy', "['slash']", "['unseen']", '581.0', "['True']"]
            print(rawLIST[0])
            print(type(rawLIST[0]))
            
            # collect the sub_num
            sub_idLIST.append(rawLIST[0])
            # calculate and collect the trial count
            trials_count += 1
            trialLIST.append(trials_count)
            
        print(sub_idLIST)
        print(trialLIST)
            
        """
            if rawLIST[2] in High_CDpwLIST:
                #print("High CD pw: ", rawLIST)
                H_CD_rawLIST.append(rawLIST)
            elif rawLIST[2] in Low_CDpwLIST:
                #print("Low CD pw: ", rawLIST)
                L_CD_rawLIST.append(rawLIST)
            else:   
                pass
        """

        """
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
        #print("H_CD_rawLIST", H_CD_rawLIST)  # [['022', '2022-05-14', 'aegliy', "['z']", "['seen']", '1982.0', "['True']"], ['022', '2022-05-14', 'vaesow', "['z']", "['seen']", '726.0', "['True']"],.....]]
        #print(len(H_CD_rawLIST))
        #print("L_CD_rawLIST", L_CD_rawLIST)  # same as "H_CD_rawLIST"
        #print(len(L_CD_rawLIST))
        
        """
    """
    # wanted columnLIST
    sub_LIST = []
    conditionALL_LIST = []
    trialsALL_LIST = []
    itemALL_LIST = []
    timesLIST = []
    ACCall_LIST = []
    RTfinalLIST = []
    
    
    
    
    # making the wanted info into the List form for future use
    sub_idLIST.append(sub_num)
    
    # For Mean data
    H_total_rawRT_LIST.append(H_mean_subFLOAT)
    L_total_rawRT_LIST.append(L_mean_subFLOAT)
    H_total_finalRT_LIST.append(H_final_mean_subFLOAT)
    L_total_finalRT_LIST.append(L_final_mean_subFLOAT)
    
    # For Correctness data
    sub_AllrawCorrect_LIST.append(PLDT_correct_subDICT["PLDT-total Correctness"])
    H_total_rawCorrect_LIST.append(H_PLDT_correct_subDICT["H-CD PLDT Correctness"])
    L_total_rawCorrect_LIST.append(L_PLDT_correct_subDICT["L-CD PLDT Correctness"])
    H_total_finalCorrect_LIST.append(n_H_PLDT_correct_subDICT["New H-CD PLDT Correctness"])
    L_total_finalCorrect_LIST.append(n_L_PLDT_correct_subDICT["New L-CD PLDT Correctness"])
    
    # For Self-rating data
    ALL_ratingINT_LIST.append(ALL_ratingMeanINT)
    H_ratingINT_LIST.append(H_ratingMeanINT)
    L_ratingINT_LIST.append(L_ratingMeanINT)
    
    # For self-paced reading data
    ALL_readingT_msINT_LIST.append(ALL_readingT_msINT)
    H_readingT_msINT_LIST.append(H_readingT_msINT)
    L_readingT_msINT_LIST.append(L_readingT_msINT)
    ALL_readingT_minINT_LIST.append(ALL_readingT_minFLOAT)
    H_readingT_minINT_LIST.append(H_readingT_minFLOAT)
    L_readingT_minINT_LIST.append(L_readingT_minFLOAT)
    
    
    # Saving the analyzed results into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                             '(ms)H_raw_RTMean':H_total_rawRT_LIST,
                             '(ms)H_final_RTMean':H_total_finalRT_LIST,
                             '(ms)L_raw_RTMean':L_total_rawRT_LIST,
                             '(ms)L_final_RTMean':L_total_finalRT_LIST,
                             
                             '(%)ALL_Correctness':sub_AllrawCorrect_LIST,
                             '(%)H_raw_Correctness':H_total_rawCorrect_LIST,
                             '(%)H_final_Correctness':H_total_finalCorrect_LIST,
                             '(%)L_raw_Correctness':L_total_rawCorrect_LIST,
                             '(%)L_final_Correctness':L_total_finalCorrect_LIST,
                             
                             'Self_rating_Mean':ALL_ratingINT_LIST,
                             'H_Self_rating_Mean':H_ratingINT_LIST,
                             'L_Self_rating_Mean':L_ratingINT_LIST,
                             
                             '(ms)Self_readingT_msMean':ALL_readingT_msINT_LIST,
                             '(ms)H_Self_readingT_msMean':H_readingT_msINT_LIST,
                             '(ms)L_Self_readingT_msMean':L_readingT_msINT_LIST,
                             '(min)Self_readingT_minMean':ALL_readingT_minINT_LIST,
                             '(min)H_Self_readingT_minMean':H_readingT_minINT_LIST,
                             '(min)L_Self_readingT_minMean':L_readingT_minINT_LIST,
                             
                             })

    file_name = '000_004-035_PLDT_analyzed_results.csv'
    save_path = result_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
    """
