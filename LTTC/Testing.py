#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import csv
from pprint import pprint

if __name__ == "__main__":

    result_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/"  # Testing
    sub_id = str(input("Subject: "))
    
    
    with open(result_data_path + "S%s_Reading_task.csv" %sub_id, "r", encoding="UTF-8") as csvfile:  #, newline=''
        result_csvLIST = csvfile.read().split("\n")
        pprint(result_csvLIST)