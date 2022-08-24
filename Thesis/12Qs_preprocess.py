#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
import re
import csv

def correct_time(Start_timeFLOAT, End_timeFLOAT, stim_onsetFLOAT):
    actual_timeFLOAT = stim_onsetFLOAT*(End_timeFLOAT-Start_timeFLOAT)+(Start_timeFLOAT)
    return actual_timeFLOAT


if __name__ == "__main__":
    
    """
    data_path = "/Users/ting-hsin/Downloads/碩論(二外語言習得的腦科學特徵與譯文判讀之關聯與影響)/新碩論主題/Ding-Thesis_ExpMaterials/"
    
    
    with open(data_path + "(MRI)code_comprehension_questions.txt", "r", encoding = "UTF-8") as txtFile:
        textLIST = txtFile.read().split("\t\n")
        pprint(textLIST)
        print(type(textLIST))
        print(len(textLIST))
    """
    """
        final_textLIST = []
        tmpLIST = []
        for row in textLIST:
            tmpLIST = row.split("\n")
            #print(tmpLIST)
            for item in tmpLIST:
                if len(item) <2:
                    tmpLIST.remove(item)
                else:
                    item = re.sub('\s|\d\t\s', " ", item)
                    pprint(item)
                print(tmpLIST)
            #final_textLIST.append(tmpLIST)
            
        #pprint(final_textLIST)
            #row = re.sub('\s\t\s', " ", row)
            #pprint(row)
            """
    
    #((z-7879)/(65890-7879)) = 0.4
    z = 0.4*(65890-7879)+(7879)
    print("correct ans: ", z)
    
    ans = correct_time(7879, 65890, 0.4)
    print("func ans: ", ans)
    """
    def correct_time(Start_timeFLOAT, End_timeFLOAT, stim_onsetFLOAT, actual_timeFLOAT):
        actual_timeFLOAT = stim_onsetFLOAT*(End_timeFLOAT-Start_timeFLOAT)+(Start_timeFLOAT)
        return actual_timeFLOAT
    """
    
        


