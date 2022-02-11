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
        
        for row in fileLIST:
            tmpLIST = row.replace(',"', ', ""').split(', "') #.replace(', "', ',"').split(', "')
            #rowLIST = tmpLIST[1]
            print(tmpLIST[0])
            #print(tmpLIST[1])
            #print(type(tmpLIST[1]))
            #print(len(rowLIST))
            #contentLIST = row.split(",")
            #print(contentLIST)
            
            #exclude the blank LIST and the first LIST

        """
        for item in rowLIST:
            print(len(item))
        """    
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