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
    
    with open (data_path + "LTTC-modified_materials_3.csv", "r", encoding = "utf-8") as raw_file:
        fileLIST = raw_file.read().split("\n")
        #pprint(fileLIST[1])
        
        """
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
                
        print(tmpLIST_1)
        #print(len(tmpLIST_1))
        """
        
        # preprocess the modified texts
        for row in fileLIST:
            if ',150' in row:
                tmpLIST = row.replace(',150', '///').split('///,"')
                #print(tmpLIST)
                #print(len(tmpLIST))
                #print(tmpLIST[1])
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
        """
        # excluding the unwanted info from the raw texts
        # save all the texts into one list, but it is a whole text per unit  # json file = LTTC-rawText_OneLIST.json
        for n_row in tmpLIST_1:
            textLIST = n_row[1].split(", , ,")
            tmpLIST_2.extend([textLIST[0]])
            
        pprint(tmpLIST_2)
        #pprint(len(tmpLIST_2))
        """
        
        #"""
        # excluding the unwanted info from the modified texts
        # save all the texts into one list, but it is a whole text per unit  # json file = LTTC-rawText_OneLIST.json
        for n_row in tmpLIST_1:
            textLIST = n_row[1].split('",')
            #print(textLIST)
            #print(len(textLIST))
            #print(textLIST[0])
            
            tmpLIST_2.extend([textLIST[0]])
            
        pprint(tmpLIST_2)
        #pprint(len(tmpLIST_2))
        #"""
       
        
        
        with open(data_path + 'LTTC-modifiedText_OneLIST.json', "w", newline='', encoding="UTF-8") as jsonfile:
            json.dump(tmpLIST_2, jsonfile, ensure_ascii=False)
            