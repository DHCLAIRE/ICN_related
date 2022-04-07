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
    
    #texts_totalDICT = {}
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
    """
    # reload the texts
    with open (text_data_path + "LTTC-modifiedText_OneLIST_blank.json", "r", encoding = "utf-8") as jfile_2:
        textLIST = json.load(jfile_2)
        #pprint(textLIST[0:10])
        
        # for 
        for count in range(10):
            tmpDICT = {'{}'.format(count+1) : textLIST[count:count+10]}  # This result is wrong!!  #textLIST[0:10]} & textLIST[10:10]}
            texts_totalDICT.update(tmpDICT)
        pprint(texts_totalDICT)
        
    # 6_divided all the pre-selected texts into the High-CD and Low-CD sets
     # ALL Sets of Texts  >> the following should be able to set it as a loop
        
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
        
        
        
        # High-CD setsDICT (3/4/5/6/7)
        sets_3_DICT = {'3':textLIST[20:30]}
        sets_4_DICT = {'4':textLIST[30:40]}
        sets_5_DICT = {'5':textLIST[40:50]}
        sets_6_DICT = {'6':textLIST[50:60]}
        sets_7_DICT = {'7':textLIST[60:70]}
        texts_high_CD_setDICT.update(sets_3_DICT)
        texts_high_CD_setDICT.update(sets_4_DICT)
        texts_high_CD_setDICT.update(sets_5_DICT)
        texts_high_CD_setDICT.update(sets_6_DICT)
        texts_high_CD_setDICT.update(sets_7_DICT)
        #pprint(texts_high_CD_setDICT)
        print(len(texts_high_CD_setDICT))

        # Low-CD setsDICT (1/2/8/9/10)
        sets_1_DICT = {'1':textLIST[0:10]}
        sets_2_DICT = {'2':textLIST[10:20]}
        sets_8_DICT = {'8':textLIST[70:80]}
        sets_9_DICT = {'9':textLIST[80:90]}
        sets_10_DICT = {'10':textLIST[90:]}
        
        texts_low_CD_setDICT.update(sets_1_DICT)
        texts_low_CD_setDICT.update(sets_2_DICT)
        texts_low_CD_setDICT.update(sets_8_DICT)
        texts_low_CD_setDICT.update(sets_9_DICT)
        texts_low_CD_setDICT.update(sets_10_DICT)
        #pprint(texts_low_CD_setDICT)
        print(len(texts_low_CD_setDICT))
        
        
        # texts_high_CD_setLIST = [345, 456, 567, 367, 347] >> we randomly choose one the set from these 5 sets
        tHigh_345LIST = []
        tHigh_345LIST.append(sets_3_LIST)
        tHigh_345LIST.append(sets_4_LIST)
        tHigh_345LIST.append(sets_5_LIST)
        #pprint(tHigh_345LIST)
        
        stim_345_LIST = []
        tmpLIST_3 = sample(sets_3_LIST, 5)
        tmpLIST_4 = sample(sets_4_LIST, 5)
        tmpLIST_5 = sample(sets_5_LIST, 5)
        stim_345_LIST.extend(tmpLIST_3)
        stim_345_LIST.extend(tmpLIST_4)
        stim_345_LIST.extend(tmpLIST_5)
        #print(stim_345_LIST)
        #print(len(stim_345_LIST))
        
        realwords = ["premier", "butler" ,"thesis" ,"gimmick" ,"yogurt" , "palette", "eclipse", "marrow", "locust", "cabaret"]
        tmpLIST_X = []
        #for realw in range(len(stim_345_LIST)):
        for t in stim_345_LIST:
            print(len(t))
            if "thesis" in t:
                print("There's a word in here!")
                t.replace("thesis", "{}")
                pprint(t)
            elif "gimmick" in t:
                print("There's a word in here!")
                t.replace("gimmick", "{}")
                pprint(t)
            elif "yogurt" in t:
                print("There's a word in here!")
                t.replace("yogurt", "{}")
                pprint(t)
            else:
                print("NONE")
                #pass
            
            for realw in realwords:
                if realw in t:
                    pprint(t)
                    #t.replace("{}".format(realw), "{}")
                    #pprint(t)
                    #tmpSTR = [t]
                    #tmpLIST_X.extend(tmpSTR)
                else:
                    pass
            #stim_345_LIST = tmpLIST_X
        #pprint(stim_345_LIST)
        #pprint(len(stim_345_LIST))
        
        
        
        tHigh_456LIST = []
        tHigh_567LIST = []
        tHigh_367LIST = []
        tHigh_347LIST = []
        
        # Low-CD sets
        # texts_low_CD_setLIST = [128, 289, 890, 190, 120] >> we randomly choose one the set from these 5 sets
        tlow_128LIST = []
        tlow_289LIST = []
        tlow_890LIST = []
        tlow_190LIST = []
        tlow_120LIST = []
        """

