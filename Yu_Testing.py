#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
import csv
import json

if __name__ == "__main__":
    
    data_path = "/Users/ting-hsin/Downloads/"
    tmpLIST = []
    #tmpLIST_2 = []
    #tmpLIST_3 = []
    #tmpLIST_4 = []
    #tmpLIST_5 = []
    #tmpLIST_6 = []
    #raw_pseudowordsLIST = []


    with open (data_path + "ceg178study2_sub01_1.csv", "r", encoding = "utf-8") as raw_file:
        fileLIST = raw_file.read().split("\n")
        #pprint(fileLIST)
        
        for i in fileLIST:
            tmpLIST = i.split(",")
            print(tmpLIST[2])
            print(type(tmpLIST))