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



if __name__ == "__main__":
    result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"