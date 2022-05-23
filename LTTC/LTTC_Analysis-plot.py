#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from pprint import pprint
import csv
import json
import random
from random import sample
import numpy as np
from datetime import datetime,date
import pandas as pd
import matplotlib.pyplot as plt
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

if __name__ == "__main__":
    
    result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"
    
    resultLIST = []
    x_LIST = []
    y_LIST = []
    
    
    with open (result_data_path + "PLDT_analyzed_results.csv", "r", encoding = "utf-8") as csvfile:
        resultLIST = csvfile.read().split("\n")
        resultLIST.pop(0)
        resultLIST = LISTblankEraser(resultLIST)
        
        for row in resultLIST:
            rawLIST = row.split(",")
            
            x_LIST.append(rawLIST[1])
            y_LIST.append(rawLIST[5])
        print(x_LIST)
        print(y_LIST)
        
        
