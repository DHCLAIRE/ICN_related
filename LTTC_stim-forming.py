#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
import csv
import json

'''
Steps: 
1. create a list that only have 12 pseudowords
2. import the pseudoword list
3. randomly select 6 out of the list of 12 pseudowords as the target words
4. select 3 out of the 6 target words and divided 3-3 into High-CD and Low-CD conditions
5. import all the pre-selected bunch of texts
6. randomly selelct a pair set of High-CD and Low-CD texts
7. insert the assigned pseudowords into the pair set of High-CD and Low-CD texts
8. 
'''


if __name__ == "__main__":
    data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/2nd_Stim-Materials/"
    tmpLIST = []
    tmpLIST_2 = []
    
    with open (data_path + "2nd_Pseudowords_12.csv", "r", encoding = "utf-8") as raw_file:
        fileLIST = raw_file.read().split("\n")
        #pprint(fileLIST)
        
    for i in fileLIST:
        tmpLIST = i.split(",")
        
        #print(tmpLIST)
        #print(type(tmpLIST))
        for z in tmpLIST:
            if len(z) == 0:
                tmpLIST.remove(z)
                print(tmpLIST)
            else:
                pass
        tmpLIST_2.append(tmpLIST)
    pprint(tmpLIST_2)