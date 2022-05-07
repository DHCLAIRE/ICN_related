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
        
        # finding the wanted H & L CD response
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
        print(H_rtLIST)
        print(len(H_rtLIST))
        print(sum(np.array(H_rtLIST)))
        print(round(np.mean(np.array(H_rtLIST)),3))
        
        for row in L_CD_rawLIST:
            L_rtLIST.append(float(row[5]))
            if 0. in L_rtLIST:
                L_rtLIST.remove(0.0)
            else:
                pass
        print(L_rtLIST)
        print(len(L_rtLIST))
        print(sum(np.array(L_rtLIST)))
        print(round(np.mean(np.array(L_rtLIST)),3))
        
        
        """
            # calculate PLDT_mean (H & L) per sub
            rtLIST.append(float(rawLIST[5]))
        print(rtLIST)
        print(len(rtLIST))
        
        # exclude the N/A response
        for rt in rtLIST:
            if 0. in rtLIST:
                rtLIST.remove(0.0)
            else:
                pass
        print(rtLIST)
        print(len(rtLIST))
        
        #print(np.array(rtLIST))
        #print(len(np.array(rtLIST)))
        #print(type(np.array(rtLIST)))
        ##rtARRAY = np.array(rtLIST)
        """
        """
        print("High-CD RT LIST = ", High_CDRT_LIST)
        print(len(High_CDRT_LIST))
        print("Low-CD RT LIST = ", Low_CDRT_LIST)
        print(len(Low_CDRT_LIST))
        
        for HighRT_STR in High_CDRT_LIST:
            if len(HighRT_STR) == 1:
                High_CDRT_LIST.remove(HighRT_STR)
                final_High_RT_LIST = High_CDRT_LIST
            else:
                final_High_RT_LIST = High_CDRT_LIST
        print(final_High_RT_LIST)
        print(len(final_High_RT_LIST))
        
        for LowRT_STR in Low_CDRT_LIST:
            if len(LowRT_STR) == 1:
                Low_CDRT_LIST.remove(LowRT_STR)
                final_Low_RT_LIST = Low_CDRT_LIST
            else:
                final_Low_RT_LIST = Low_CDRT_LIST
                
        print(final_Low_RT_LIST)
        print(len(final_Low_RT_LIST))
        
        High_Mean = RT_Mean(final_High_RT_LIST)  #round(Sum(final_High_RT_LIST)/len(final_High_RT_LIST), 4)
        Low_Mean = RT_Mean(Low_CDRT_LIST)
        
        print(High_Mean)
        print(type(High_Mean))
        print(Low_Mean)
        print(type(Low_Mean))
        
        RT_LIST = ['1481', '948', '821', '1186', ' ', '0']
        
        
        for STR in RT_LIST:
            if len(STR) == 1:
                if STR == '0' or STR != '0':
                    print("Ya")
                    RT_LIST.remove(STR)
                    final_RT_LIST = RT_LIST
                else:
                    pass
            else:
                final_RT_LIST = RT_LIST
                
        print(final_RT_LIST)
        print(len(final_RT_LIST))
        
        
    # For SelfPRT_Mean
    #with
    """