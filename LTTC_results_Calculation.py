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
    
    
    with open (result_data_path + "001_LDT_results.csv", "r", encoding = "utf-8") as csvfile:
        resultLIST = csvfile.read().split("\n")
        #print(resultLIST)
        #print(len(resultLIST))
        
        for row in resultLIST:
            tmpLIST = row.split(",")
            print(tmpLIST)
            print(len(tmpLIST))
            print(type(tmpLIST))
            


