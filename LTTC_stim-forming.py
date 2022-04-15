#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Steps: 
1. (DONE)create a list that only have 12 pseudowords
2. (DONE)import the pseudoword list
3. (DONE)randomly select 6 out of the list of 12 pseudowords as the target words
4. (DONE)select 3 out of the 6 target words and divided 3-3 into High-CD and Low-CD conditions
5. (DONE)import all the pre-selected bunch of texts
6. (DONE)divided all the pre-selected texts into the High-CD and Low-CD sets
7. (KIND OF?)randomly selelct a pair set of High-CD and Low-CD texts
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
    result_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/2nd_Stim-results_selfPRT_PLDT/"
    text_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/"
    textSets_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/LTTC_TextSets/"
    tmpLIST = []
    tmpLIST_2 = []
    pseudoLIST = []
    targetPseudoLIST = []
    controlPseudoLIST = []
    words_high_CD_setLIST = []
    words_low_CD_setLIST = []
    texts_high_CD_setLIST = []
    texts_low_CD_setLIST = []
    
    #texts_totalDICT = {}
    #texts_high_CD_setDICT = {}
    #texts_low_CD_setDICT = {}
    
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
    with open(stim_data_path + 'LTTC-pseudowordLIST.json', "w", newline='', encoding="UTF-8") as jsonfile:
        json.dump(pseudoLIST, jsonfile, ensure_ascii=False)
        """
    #"""
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
    #"""
    """
    # reload the texts
    with open (text_data_path + "LTTC-modifiedText_OneLIST_present.json", "r", encoding = "utf-8") as jfile_2:
        textLIST = json.load(jfile_2)
        #pprint(textLIST[0:10])
        
        # divide all the sets into an individual LIST by topic
        # High-CD setsLIST (3/4/5/6/7)
        sets_3_LIST = textLIST[20:30]
        sets_4_LIST = textLIST[30:40]
        sets_5_LIST = textLIST[40:50]
        sets_6_LIST = textLIST[50:60]
        sets_7_LIST = textLIST[60:70]
        
        # Low-CD setsDICT (1/2/8/9/10)
        sets_1_LIST = textLIST[0:10]
        sets_2_LIST = textLIST[10:20]
        sets_8_LIST = textLIST[70:80]
        sets_9_LIST = textLIST[80:90]
        sets_10_LIST = textLIST[90:]
        
        print(sets_3_LIST)
    
        # save all the sets into an individual json file
        with open(textSets_data_path + "sets_10_LIST.json", "w", newline='', encoding="UTF-8") as setsfile:
            json.dump(sets_10_LIST, setsfile, ensure_ascii=False)
        """

    
    textSetsLIST_High = []
    textSetsLIST_Low = []
    new_High_textSetsLIST = []
    new_Low_textSetsLIST = []
    High_stimLIST = []
    High_stim_SetLIST = []
    Low_stimLIST = []
    Low_stim_SetLIST = []
    total_stimSetLIST = []
    suffledTotalT_LIST = []
    
    # for calling out the sets individually
    HightSetsLIST = []
    LowtSetsLIST = []
    
    # High_CD Set TEXTS
    # texts_high_CD_setLIST = [345, 456, 567, 367, 347]
    HighCD_CallingLIST = [["3", "4", "5"], ["4", "5", "6"], ["5", "6", "7"], ["3", "6", "7"], ["3", "4", "7"]]
    LowCD_CallingLIST = [["1", "2", "8"], ["2", "8", "9"], ["8", "9", "10"], ["1", "9", "10"], ["1", "2", "10"]]
    HightSetsLIST = random.sample(HighCD_CallingLIST, 1)
    LowtSetsLIST = random.sample(LowCD_CallingLIST, 1)
    print(HightSetsLIST)
    print(HightSetsLIST[0][0])
    print(LowtSetsLIST)
    print(LowtSetsLIST[0][0])
    
    
    for sets in range(3):
        # High_CD Set TEXTS
        with open (textSets_data_path + "sets_{}_LIST.json".format(HightSetsLIST[0][sets]), "r", encoding = "utf-8") as jfile_3:
            textSetsLIST_High = json.load(jfile_3)
            
            # randomly select 5 texts from the json file
            High_stimLIST = random.sample(textSetsLIST_High, 5)
            #pprint(High_stimLIST)
            #print(len(High_stimLIST))

            # replace {} to the assigned pseudowords by different condition
            for tSTR in High_stimLIST:
                new_tSTR = tSTR.replace("{}", words_high_CD_setLIST[sets])
                #pprint(new_tSTR)
                new_High_textSetsLIST.extend([new_tSTR])
                
        # Low_CD Set TEXTS
        # texts_low_CD_setLIST = [128, 289, 890, 190, 120]
        with open (textSets_data_path + "sets_{}_LIST.json".format(LowtSetsLIST[0][sets]), "r", encoding = "utf-8") as jfile_4:
            textSetsLIST_Low = json.load(jfile_4)
                    
            # randomly select 5 texts from the json file
            Low_stimLIST = random.sample(textSetsLIST_Low, 5)
            #pprint(Low_stimLIST)
            #print(len(Low_stimLIST))
        
            # replace {} to the assigned pseudowords by different condition
            for tSTR in Low_stimLIST:
                new_tSTR = tSTR.replace("{}", words_low_CD_setLIST[sets])
                #pprint(new_tSTR)
                new_Low_textSetsLIST.extend([new_tSTR])
                
    pprint(new_High_textSetsLIST)
    print(len(new_High_textSetsLIST))
    pprint(new_Low_textSetsLIST)
    print(len(new_Low_textSetsLIST))
    
    total_stimSetLIST.extend(new_High_textSetsLIST)
    total_stimSetLIST.extend(new_Low_textSetsLIST)
    
    print(len(total_stimSetLIST))
    random.shuffle(total_stimSetLIST)