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
    #result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"
    result_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/2nd_Stim-results_selfPRT_PLDT/"
    
    # wanted columnLIST
    sub_LIST = []
    conditionALL_LIST = []
    trialsALL_LIST = []
    itemALL_LIST = []
    timesLIST = []
    ACCall_LIST = []
    RTfinalLIST = []
    
    
    
    for z in range(1):
        # raw data
        resultLIST = []
        rawLIST = []
        pseudoLIST = []
        controlPseudoLIST = []
        High_CDpwLIST = []
        Low_CDpwLIST = []
        
        # wanted columnLIST
        sub_idLIST = []
        conditionLIST = []
        trialLIST = []
        itemLIST = []
        ACCLIST = []
        TandF_LIST = []
        RTLIST = []
        countLIST = []
        countTYPE_LIST = []
        countALL_LIST = []
        
        sub_num = "0{0:02d}".format(z+7)
        # Open the pseudowordDICT for the further indications
        with open (result_data_path + "{}_pseudowordsDICT.json".format(sub_num), "r", encoding = "utf-8") as jfile:
            pseudoDICT = json.load(jfile)
            #pprint(pseudoDICT)
            
            controlPseudoLIST.extend(pseudoDICT["The ControlPseudo group_6"])
            High_CDpwLIST.extend(pseudoDICT["High_CD condition pseudowords_3"])
            Low_CDpwLIST.extend(pseudoDICT["Low_CD condition pseudowords_3"])
            print(controlPseudoLIST)
            print(High_CDpwLIST)
            print(Low_CDpwLIST)
        
        # For LDT results calculation  >> should I add True/False calculation???
        with open (result_data_path + "{}_LDT_results.csv".format(sub_num), "r", encoding = "utf-8") as csvfile:
            resultLIST = csvfile.read().split("\n")
            #pprint(resultLIST)
            #print(len(resultLIST))
            resultLIST.pop(0)   # exclude t4he headers
            #print(len(resultLIST))
        
            # exclude the blank row
            resultLIST = LISTblankEraser(resultLIST)
        
        trials_count = 0
        
        count_H_0 = 0
        count_H_1 = 0
        count_H_2 = 0
        count_H_3 = 0
        count_H_4 = 0
        count_H_5 = 0
        
        count_L_0 = 0
        count_L_1 = 0
        count_L_2 = 0
        count_L_3 = 0
        count_L_4 = 0
        count_L_5 = 0
        
        count_C_0 = 0
        count_C_1 = 0
        count_C_2 = 0
        count_C_3 = 0
        count_C_4 = 0
        count_C_5 = 0
        
        count_tmpLIST = []
        conditionLIST
        conditionALLLIST = []
        
        for row in resultLIST:
            rawLIST = row.split(",")
            print(rawLIST)   # ['007', '2022-04-19', 'chaeviy', "['slash']", "['unseen']", '581.0', "['True']"]
            
            # collect the sub_num
            sub_idLIST.append(rawLIST[0])
            
            # calculate and collect the trial count
            trials_count += 1
            trialLIST.append(trials_count)
            
            # collect the pw item
            itemLIST.append(rawLIST[2])
            
            # collect the RT pf each LDT
            RTLIST.append(round(float(rawLIST[5]), 4))
            
            # collect the accuracy of the LDT
            if rawLIST[6] == "['True']":
                ACC = 1
            elif rawLIST[6] == "['False']":
                ACC = 0
            else:
                ACC = 99
            ACCLIST.append(ACC)
            
            # collect the pw conditions
            if rawLIST[2] in controlPseudoLIST:
                count_indexINT = controlPseudoLIST.index(rawLIST[2])
                if count_indexINT == 0:
                    count_C_0 += 1
                    count_tmpLIST = [count_C_0]
                    conditionLIST = ["C"]
                if count_indexINT == 1:
                    count_C_1 += 1
                    count_tmpLIST = [count_C_1]
                    conditionLIST = ["C"]
                if count_indexINT == 2:
                    count_C_2 += 1
                    count_tmpLIST = [count_C_2]
                    conditionLIST = ["C"]
                if count_indexINT == 3:
                    count_C_3 += 1
                    count_tmpLIST = [count_C_3]
                    conditionLIST = ["C"]
                if count_indexINT == 4:
                    count_C_4 += 1
                    count_tmpLIST = [count_C_4]
                    conditionLIST = ["C"]
                if count_indexINT == 5:
                    count_C_5 += 1
                    count_tmpLIST = [count_C_5]
                    conditionLIST = ["C"]
                else:
                    pass
                
            elif rawLIST[2] in High_CDpwLIST:
                count_indexINT = High_CDpwLIST.index(rawLIST[2])
                
                if count_indexINT == 0:
                    count_H_0 += 1
                    count_tmpLIST = [count_H_0]
                    conditionLIST = ["H"]
                if count_indexINT == 1:
                    count_H_1 += 1
                    count_tmpLIST = [count_H_1]
                    conditionLIST = ["H"]
                if count_indexINT == 2:
                    count_H_2 += 1
                    count_tmpLIST = [count_H_2]
                    conditionLIST = ["H"]
                if count_indexINT == 3:
                    count_H_3 += 1
                    count_tmpLIST = [count_H_3]
                    conditionLIST = ["H"]
                if count_indexINT == 4:
                    count_H_4 += 1
                    count_tmpLIST = [count_H_4]
                    conditionLIST = ["H"]
                if count_indexINT == 5:
                    count_H_5 += 1
                    count_tmpLIST = [count_H_5]
                    conditionLIST = ["H"]
                else:
                    pass
                    
                
            elif rawLIST[2] in Low_CDpwLIST:
                count_indexINT = Low_CDpwLIST.index(rawLIST[2])
                
                if count_indexINT == 0:
                    count_L_0 += 1
                    count_tmpLIST = [count_L_0]
                    conditionLIST = ["L"]
                if count_indexINT == 1:
                    count_L_1 += 1
                    count_tmpLIST = [count_L_1]
                    conditionLIST = ["L"]
                if count_indexINT == 2:
                    count_L_2 += 1
                    count_tmpLIST = [count_L_2]
                    conditionLIST = ["L"]
                if count_indexINT == 3:
                    count_L_3 += 1
                    count_tmpLIST = [count_L_3]
                    conditionLIST = ["L"]
                if count_indexINT == 4:
                    count_L_4 += 1
                    count_tmpLIST = [count_L_4]
                    conditionLIST = ["L"]
                if count_indexINT == 5:
                    count_L_5 += 1
                    count_tmpLIST = [count_L_5]
                    conditionLIST = ["L"]
                else:
                    pass
                    #print("Wrong")
                    
            else:
                print("WRONG!!!", rawLIST[2])
            countALL_LIST.extend(count_tmpLIST)
            conditionALLLIST.extend(conditionLIST)
        # to set the first apprearance pw as the 
        for k in range(12):
            conditionALLLIST[k] = "N"
            # condition & times need to recalculate!!!!!! & and also one colunm that indicates the reason of the deleted responses
            
        print(sub_idLIST)
        print(trialLIST)
        print(itemLIST)
        print(RTLIST)
        print(ACCLIST)
        print(countALL_LIST)
        print(conditionALLLIST)
        
        '''
        # wanted columnLIST
        sub_LIST = []
        conditionALL_LIST = []
        trialsALL_LIST = []
        itemALL_LIST = []
        timesLIST = []
        ACCall_LIST = []
        RTfinalLIST = []
        '''
        
        
        # making the wanted info into the List form for future use
        sub_LIST.append(sub_idLIST)
        conditionALL_LIST.append(conditionALLLIST)
        trialsALL_LIST.append(trialLIST)
        itemALL_LIST.append(itemLIST)
        timesLIST.append(countALL_LIST)
        ACCall_LIST.append(ACCLIST)
        RTfinalLIST.append(RTLIST)
        
        # Saving the analyzed results into csv file
        dataDICT = pd.DataFrame({'Sub_id':sub_LIST,
                                 'Condition':conditionALL_LIST,
                                 'Trials':trialsALL_LIST,
                                 'Item':itemALL_LIST,
                                 'Times':timesLIST,
                                 'ACC':ACCall_LIST,
                                 'RT':RTfinalLIST
                                 })

        file_name = '000_007-036_PLDT_raw_results.csv'
        save_path = result_data_path + file_name
        dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

