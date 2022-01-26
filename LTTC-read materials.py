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
    
    with open (data_path + "LTTC-materials.csv", "r", encoding = "utf-8") as raw_file:
        fileLIST = raw_file.read().split("\n")
        for row in fileLIST:
            rowLIST.append([row])
        for item in rowLIST:
            print(len(item))
            '''
            for content in item:
                contentLIST = content.split(",,")
            print(contentLIST)
            
            
            if len(item) == 1:
                print(item)
                #rowLIST.remove(item)
                #rowLIST = y
            else:
                pass
        #pprint(rowLIST)
        
            for loop in range(len(rowLIST)):
                if "," in item[0][0]:
                    print(item)
            
                if c == ",":
                    print(item)
                else:
                    pass
                
        #pprint(rowLIST)
        '''