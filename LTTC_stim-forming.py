#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Steps: 
1. (DONE)create a list that only have 12 pseudowords
2. (DONE)import the pseudoword list
3. (DONE)randomly select 6 out of the list of 12 pseudowords as the target words
4. (DONE)select 3 out of the 6 target words and divided 3-3 into High-CD and Low-CD conditions
5. import all the pre-selected bunch of texts
6. randomly selelct a pair set of High-CD and Low-CD texts
7. insert the assigned pseudowords into the pair set of High-CD and Low-CD texts
8. 
'''

from pprint import pprint
import csv
import json
import random
from random import sample


if __name__ == "__main__":
    data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/2nd_Stim-Materials/"
    tmpLIST = []
    tmpLIST_2 = []
    pseudoLIST = []
    targetPseudoLIST = []
    controlPseudoLIST = []
    high_CD_setLIST = []
    low_CD_setLIST = []
    
    """
    # 1_Create the pseudoword LIST and save it into json file
    
    # Open the csv file that contains the info of 12 pseudowords
    with open (data_path + "2nd_Pseudowords_12.csv", "r", encoding = "utf-8") as raw_file:
        fileLIST = raw_file.read().split("\n")
        #pprint(fileLIST)
    
    # Organized the csv into a more convenient form of structure, which is a list of lists that carry the info of each pseudoword
    for i in fileLIST:
        tmpLIST = i.split(",")
        tmpLIST_2.append(tmpLIST)
    # exclude the head title in the csv file
    tmpLIST_2.pop(0)
    print(tmpLIST_2)
    
    # Extract the pseudowords from the organized list
    for k in tmpLIST_2:
        pseudoSTR = k[0]
        pseudoLIST.extend([pseudoSTR])
    print(pseudoLIST)
    
    # Save the pseudoword LIST into a json file
    #with open(data_path + 'LTTC-pseudowordLIST.json', "w", newline='', encoding="UTF-8") as jsonfile:
        #json.d ump(pseudoLIST, jsonfile, ensure_ascii=False)
        """
    
    # 2_Import the pseudoword list (in json file form)
    with open (data_path + "LTTC-pseudowordLIST.json", "r", encoding = "utf-8") as jfile:
        pseudoLIST = json.load(jfile)
        print("12 pseudowords = ", pseudoLIST)
        
        # suffle the pseudoword list (shuffle or not, both works)
        #random.shuffle(pseudoLIST)
        #print(pseudoLIST)
        
    # 3_Randomly select 6 out of the list of 12 pseudowords as the target words
        # randomly select 6 target pseudowords from the list
        targetPseudoLIST = sample(pseudoLIST, 6)
        
        # collect other 6 pseudowords as the control group
        for t in pseudoLIST:
            if t not in targetPseudoLIST:
                controlPseudoLIST.extend([t])
            else:
                pass
            
        print("The TargetPseudo words = ", targetPseudoLIST)
        print("The ControlPseudo words = ", controlPseudoLIST)
        
    # 4_Select 3 out of the 6 target words and divided 3-3 into High-CD and Low-CD conditions
        high_CD_setLIST = sample(targetPseudoLIST, 3)
        #print("High-CD_set = ", high_CD_setLIST)
        
        for w in targetPseudoLIST:
            if w not in high_CD_setLIST:
                low_CD_setLIST.extend([w])
            else:
                pass

        print("High-CD_set = ", high_CD_setLIST)
        print("Low-CD_set = ", low_CD_setLIST)
    
    # 5_Import all the pre-selected bunch of texts