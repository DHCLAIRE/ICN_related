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
            if ',"" ' in row:
                tmpLIST = row.replace(',"" ', ', ""').split(',"') 
            else:
                tmpLIST = row.replace(',"', '///"').split('///')  
                
            # delete the blank LIST
            lenNum = len(tmpLIST)
            if lenNum == 1:
                pass
            else:
                tmpLIST_1.append(tmpLIST)
                
        #pprint(tmpLIST_1)
        #print(len(tmpLIST_1))
        
        
        for n_row in tmpLIST_1:
            textLIST = n_row[1].split(", , ,")
            textLIST.pop(1)
            tmpLIST_2.append(textLIST)
        pprint(tmpLIST_2)
        print(len(tmpLIST_2))
        
        
        with open(data_path + 'LTTC-rawText_resultLIST.json', "w", newline='', encoding="UTF-8") as jsonfile:
            json.dump(tmpLIST_2, jsonfile, ensure_ascii=False)

        