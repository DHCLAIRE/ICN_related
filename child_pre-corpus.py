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
from collections import Counter
import string   # import string library function
from pathlib import Path
import os
import re




if __name__ == "__main__":
    
    root_data_path = Path("/Volumes/Neurolang_1/Project_Assistant/Corpura/Taiwanese Mandarin Written Corpus_Children")
    
    children_data = root_data_path / "(NEW)Children"
    teenagers_data = root_data_path / "(NEW)Teenagers"
    
    years_ndarray = np.arange(106, 111) # 106~110年
    months_ndarray = np.arange(1, 13)  # 1～12月
    day_ndarray = np.arange(1, 32)  # 1~31號
    
    # call out the data from children<teenagers' folder name is different>
    
    for yearINT64 in years_ndarray:
        for monthINT64 in months_ndarray:
            folder_nameSTR = "%d年%d月" %(yearINT64, monthINT64)  #e.g. 106年1月
            children_folder_path = children_data / folder_nameSTR
            #print(children_folder_path)
            for dateINT64 in day_ndarray:
                try:
                    secL_folder_nameSTR = "%d.%.2d.%.2d"  %(yearINT64, monthINT64, dateINT64) #e.g. 106.01.01
                    txtfile_data_path = children_folder_path / secL_folder_nameSTR
                    #print(txtfile_data_path)
                    txtfile_nameSTR = os.listdir(txtfile_data_path / "/")
                    print(txtfile_nameSTR)
                    
                except:
                    print("ERROR")
                    #print(txtfile_data_path)