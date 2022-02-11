#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
import csv
import json


if __name__ == "__main__":
    data_path = "/Users/neuroling/Downloads/"
    tmpLIST_1 = []
    tmpLIST_2 = []
    tmpLIST_3 = []
    rowLIST = []
    
    with open (data_path + "LTTC-materials_2.csv", "r", encoding = "utf-8") as raw_file:
        fileLIST = raw_file.read().split("\n")
        #print(fileLIST)
        
        # preprocess the raw texts
        for row in fileLIST:
            tmpLIST = row.replace(',"', ', ""').split(', "') #.replace(', "', ',"').split(', "')  #LIST 整理未完成
            
            # delete the blank LIST
            lenNum = len(tmpLIST)
            if lenNum == 1:
                pass
            else:
                tmpLIST_1.append(tmpLIST)
                
        pprint(tmpLIST_1)
        pprint(len(tmpLIST_1))
