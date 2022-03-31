#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Steps: 
1. (DONE)create a list that only have 12 pseudowords
2. (DONE)import the pseudoword list
3. (DONE)randomly select 6 out of the list of 12 pseudowords as the target words
4. (DONE)select 3 out of the 6 target words and divided 3-3 into High-CD and Low-CD conditions
5. (DONE)import all the pre-selected bunch of texts
6. divided all the pre-selected texts into the High-CD and Low-CD sets
7. randomly selelct a pair set of High-CD and Low-CD texts
8. insert the assigned pseudowords into the pair set of High-CD and Low-CD texts
# The pseudowords need to be inseted in the texts first, and then randomly choose from the texts set??

'''


from pprint import pprint
import csv
import json
import random
from random import sample


if __name__ == "__main__":
    stim_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/2nd_Stim-Materials/"
    text_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/"
    tmpLIST = []
    tmpLIST_2 = []
    pseudoLIST = []
    targetPseudoLIST = []
    controlPseudoLIST = []
    words_high_CD_setLIST = []
    words_low_CD_setLIST = []
    texts_high_CD_setLIST = []
    texts_low_CD_setLIST = []
    
    texts_totalDICT = {}
    texts_high_CD_setDICT = {}
    texts_low_CD_setDICT = {}
    
    """
    # 1_Create the pseudoword LIST and save it into json file
    
    # Open the csv file that contains the info of 12 pseudowords
    with open (stim_data_path + "2nd_Pseudowords_12.csv", "r", encoding = "utf-8") as raw_file:
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
    #with open(stim_data_path + 'LTTC-pseudowordLIST.json', "w", newline='', encoding="UTF-8") as jsonfile:
        #json.d ump(pseudoLIST, jsonfile, ensure_ascii=False)
        """
    
    # 2_Import the pseudoword list (in json file form)
    with open (stim_data_path + "LTTC-pseudowordLIST.json", "r", encoding = "utf-8") as jfile:
        pseudoLIST = json.load(jfile)
        print("12 pseudowords = ", pseudoLIST)
        
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
        words_high_CD_setLIST = sample(targetPseudoLIST, 3)
        
        for w in targetPseudoLIST:
            if w not in words_high_CD_setLIST:
                words_low_CD_setLIST.extend([w])
            else:
                pass

        print("High-CD_set = ", words_high_CD_setLIST)
        print("Low-CD_set = ", words_low_CD_setLIST)
    
    # 5_Import all the pre-selected bunch of texts
    
    # reload the texts
    with open (text_data_path + "LTTC-modifiedText_OneLIST.json", "r", encoding = "utf-8") as jfile_2:
        textLIST = json.load(jfile_2)
        
        for count in range(10):
            tmpDICT = {'{}'.format(count+1) : textLIST[count:count+10]}
            texts_totalDICT.update(tmpDICT)
        pprint(texts_totalDICT)
        
    # High-CD sets 
    # texts_high_CD_setLIST = [345, 456, 567, 367, 347]
    
    # Low-CD sets
    # texts_low_CD_setLIST = [128, 289, 890, 190, 120]        
        
        
    # 6_divided all the pre-selected texts into the High-CD and Low-CD sets
