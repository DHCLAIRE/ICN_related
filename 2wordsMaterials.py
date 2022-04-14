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

if __name__ == "__main__":
    
    # Setting up the data_path
    data_path = "/Users/neuroling/Downloads/ICN_ExpMaterials/"
    
    rawLIST = []
    testLIST = []
    resultLIST = []
    Tone_2_3LIST  = []
    Tone_3_3LIST  = []
    Tone_3_2LIST  = []
    Tone_3_1LIST  = []
    
    
    
    with open(data_path + "雙字詞_23-33-3231.csv","r", encoding = "utf-8") as csvfile:
        rawLIST = csvfile.read().split("\n")
        print(len(rawLIST))  # 34692 in total >> should minus one for the headline
        #print(tmpLIST)
        
        for row in rawLIST :
            testLIST = row.split(",")
            #print(testLIST[:4])
            
            # 23聲雙字詞
            if "2" in testLIST[2] and "3" in testLIST[3]:
                #print("這有2-3聲雙字詞 : ", testLIST[:4])
                Tone_2_3LIST.append(testLIST)
            
            # 33聲雙字詞
            if "3" in testLIST[2] and "3" in testLIST[3]:
                #print("這有3-3聲雙字詞 : ", testLIST[:4])
                Tone_3_3LIST.append(testLIST)
                
            # 32聲雙字詞
            if "3" in testLIST[2] and "2" in testLIST[3]:
                #print("這有3-2聲雙字詞 : ", testLIST[:4])
                Tone_3_2LIST.append(testLIST)
            
            # 31聲雙字詞
            if "3" in testLIST[2] and "1" in testLIST[3]:
                #print("這有3-1聲雙字詞 : ", testLIST[:4])
                Tone_3_1LIST.append(testLIST)
                
            else:
                pass
        
        # present part
        #pprint(Tone_2_3LIST)
        print("2-3聲雙字詞LIST長度 : ", len(Tone_2_3LIST))   # 1395 組
        #pprint(Tone_3_3LIST)
        print("3-3聲雙字詞LIST長度 : ", len(Tone_3_3LIST))   # 1132 組
        #pprint(Tone_3_2LIST)
        print("3-2聲雙字詞LIST長度 : ", len(Tone_3_2LIST))   # 1484 組
        #pprint(Tone_3_1LIST)
        print("3-1聲雙字詞LIST長度 : ", len(Tone_3_1LIST))   # 1096 組
        
        
        """
        # write all the list into the csv file
        headerLIST =["first_char", "sec_char", "P1","P2","P1,3->2","first_code", "sec_code", "first_freq", "first_frating", "first_stroke", "sec_freq", "sec_frating", "sec_stroke"
                     ,"word_freq", "NB", "NB1", "NB2", "rel_HF", "rel_HF_nb1", "rel_HF_nb2", "rel_HF%", "rel_HF%_nb1", "rel_HF%_nb2", "first_mno.(rating)", "sec_mno.(rating)"]
                     
        with open(data_path + '雙字詞_3-1聲.csv', 'w', encoding = "utf-8-sig") as f:   #encoding = "utf-8-sig" >> if 中文字用"utf-8" encode會有亂碼，就用"utf-8-sig", 應該就會沒事了
            # using csv.writer method from CSV package
            write = csv.writer(f)
      
            write.writerow(headerLIST)   #(fields)
            write.writerows(Tone_3_1LIST)  #(rows)
            """
