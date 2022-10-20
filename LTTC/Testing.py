#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import csv
from pprint import pprint

if __name__ == "__main__":
    sub_id = str(input("Subject: "))
    
    result_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/" %sub_id # Testing
    
    with open(result_data_path + "S%s_Reading_task.csv" %sub_id, "r", encoding="UTF-8") as csvfile:  #, newline=''
        result_csvLIST = csvfile.read().split("\n")
        pprint(result_csvLIST)
    
    
    
    
    
    """
    # How to create a string in a 2 layers loop
    for i in range(2):
        for k in range(3):
            numSTR = str(int("%d%d" %(i, k))+1)
            #numSTR = "%02d" %(i)  # automatically fill the zero on the left side of the number if the number didn't meer 2 digits
            print(numSTR)
            """