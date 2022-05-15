#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# for stimuli
from pprint import pprint
import csv
import json
import random
from random import sample
import numpy as np
from datetime import datetime,date
import pandas as pd
from collections import Counter

def LISTblankEraser(rawLIST):
    newrawLIST = []
    for row in rawLIST:
        if len(row) == 0:
            rawLIST.pop(rawLIST.index(row))
        else:
            pass
    newrawLIST = rawLIST
    #print(len(newrawLIST))
    return newrawLIST

def Mean(resultLIST, i, typeSTR = None):
    contentLIST = []
    for row in resultLIST:
        if type(row) == list:
            rawLIST = row
            contentLIST.append(float(rawLIST[i]))
        else:
            rawLIST = row.split(",")
            contentLIST.append(float(rawLIST[i]))
    #print("{} Raw data:".format(typeSTR), contentLIST)
    old_count = len(contentLIST)
    #print(old_count)

    for RT_Int in contentLIST:
        if 0. in contentLIST:
            contentLIST.remove(0.0)
        else:
            pass
    #print("{} Exclude 0.0 data:".format(typeSTR), contentLIST)
    new_count = len(contentLIST)
    #print(new_count)
    
    exclude_countINT = old_count - new_count
    PLDTmean_subFLOAT = round(np.mean(np.array(contentLIST)),3) #ouput: H pwRT Mean : 783.167
    MeanDICT = {"{} count".format(typeSTR):len(contentLIST),"{} Mean".format(typeSTR):PLDTmean_subFLOAT, "Exclude 0.0 count": exclude_countINT}
    
    return MeanDICT


def correctness(resultLIST, typeSTR = None):
    correctnessLIST = []
    count_True = 0 
    count_False = 0
    count_NA = 0
    
    for row in resultLIST:
        #rawLIST = ListDetector(row)
        if type(row) == list:
            rawLIST = row
        else:
            rawLIST = row.split(",")
            
        if rawLIST[6] == "['True']":
            count_True += 1
            correctBOOL = 1
        elif rawLIST[6] == "['False']":
            count_False += 1
            correctBOOL = 0
        else:
            count_NA += 1
            
    total_correctFLOAT = round(count_True/(count_True + count_False)*100,2)
    correctnessDICT = {"{} Correctness".format(typeSTR): total_correctFLOAT, "{} True:".format(typeSTR): count_True, "{} False:".format(typeSTR): count_False, "{} N/A:".format(typeSTR): count_NA}
    #correctnessLIST = [count_True, count_False, count_NA, total_correctFLOAT]
    
    return correctnessDICT  #correctnessLIST,   ###count_True, count_False, count_NA, total_correctFLOAT



if __name__ == "__main__":
    result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"
    
    for z in range(3):
        # Setting up the data_path
        result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"
    
        resultLIST = []
        tmpLIST = []
    
        #剩把pseudoDICT的值叫出來
        pseudoLIST = []
        targetPseudoLIST = []
        High_CDpwLIST = []
        Low_CDpwLIST = []

        sub_num = "0{}".format(z+19)
    
        with open (result_data_path + "{}_pseudowordsDICT.json".format(sub_num), "r", encoding = "utf-8") as jfile:
            pseudoDICT = json.load(jfile)
            #pprint(pseudoDICT)
        
            #print(sub_num)
        
            targetPseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])
            High_CDpwLIST.extend(pseudoDICT["High_CD condition pseudowords_3"])
            Low_CDpwLIST.extend(pseudoDICT["Low_CD condition pseudowords_3"])
        
            #print(sub_num, "Target pw : ", targetPseudoLIST)
            #print(sub_num, "High-CD pw : ", High_CDpwLIST)
            #print(sub_num, "Low-CD pw : ", Low_CDpwLIST) # output: 003 Low-CD pw :  ['vaesow', 'payliy', 'paenliy']
            
        #pass
        # raw data
        rawLIST = []
        H_CD_rawLIST = []
        L_CD_rawLIST = []
        
        ## PER PERSON ##
        # Mean
        H_pwRT_DICT = {}
        L_pwRT_DICT = {}
        # Correctness (True & False)
        PLDT_correct_subDICT = {}
        H_PLDT_correct_subDICT = {}
        L_PLDT_correct_subDICT = {}
        # Self_rating
        rating_Mean_LIST = []
        H_CD_ratingMean_subLIST = []
        L_CD_ratingMean_subLIST = []
    
        """
        ## WHOLE GROUP ##
        # Mean
        #H_PLDTmean_allLIST = []
        #L_PLDTmean_allLIST = []
        ## SD
        #H_PLDTsd_allLIST = []
        #L_PLDTsd_allLIST = []
    """
    
        # For LDT results calculation  >> should I add True/False calculation???
        with open (result_data_path + "{}_LDT_results.csv".format(sub_num), "r", encoding = "utf-8") as csvfile:
            resultLIST = csvfile.read().split("\n")
            #print(resultLIST)
            #print(len(resultLIST))
            resultLIST.pop(0)   # exclude the headers
            #print(len(resultLIST))
        
            # exclude the blank row
            resultLIST = LISTblankEraser(resultLIST)

        # Finding the wanted H & L CD response, and then calculate the Mean of H & L pwRT
        for row in resultLIST:
            rawLIST = row.split(",")
            if rawLIST[2] in High_CDpwLIST:
                #print("High CD pw: ", rawLIST)
                H_CD_rawLIST.append(rawLIST)
            elif rawLIST[2] in Low_CDpwLIST:
                #print("Low CD pw: ", rawLIST)
                L_CD_rawLIST.append(rawLIST)
            else:   
                pass
        #print(H_CD_rawLIST)
        #print(len(H_CD_rawLIST))
        #print(L_CD_rawLIST)
        #print(len(L_CD_rawLIST))
    
        # Calculate the RT Mean of the H & L PLDT
        H_pwRT_DICT = Mean(H_CD_rawLIST,5 , "High-CD RT")  #{'High-CD RT count': 30, 'High-CD RT Mean': 783.167, 'Exclude 0.0 count': 0}
        L_pwRT_DICT = Mean(L_CD_rawLIST,5 , "Low-CD RT")
        #print(H_pwRT_DICT)
        #print(L_pwRT_DICT)

        # Calculate the Correctness of all, and H & L PLDT, there's three in total
        PLDT_correct_subDICT = correctness(resultLIST, "PLDT-total")
        H_PLDT_correct_subDICT = correctness(H_CD_rawLIST, "H-CD PLDT")
        L_PLDT_correct_subDICT = correctness(L_CD_rawLIST, "L-CD PLDT")  # ouput = ([27, 2, 1, 93.1], {'Correct :': 27, 'False :': 2, 'N/A :': 1, 'Correctness': 93.1}) # type = <class 'tuple'>
    
        print(PLDT_correct_subDICT)
        #print(H_PLDT_correct_subDICT)
        #print(L_PLDT_correct_subDICT)
        #print(type(H_PLDT_correct_subDICT))
        
    
        print("{}:".format(sub_num), H_pwRT_DICT["High-CD RT Mean"], L_pwRT_DICT["Low-CD RT Mean"],PLDT_correct_subDICT["PLDT-total Correctness"],H_PLDT_correct_subDICT["H-CD PLDT Correctness"],L_PLDT_correct_subDICT["L-CD PLDT Correctness"])
        #print(H_pwRT_DICT["High-CD RT Mean"], L_pwRT_DICT["Low-CD RT Mean"],PLDT_correct_subDICT["PLDT-total Correctness"],H_PLDT_correct_subDICT["H-CD PLDT Correctness"],L_PLDT_correct_subDICT["L-CD PLDT Correctness"])
    
    
        """
    resultLIST = []
    tmpLIST = []

    #剩把pseudoDICT的值叫出來
    pseudoLIST = []
    targetPseudoLIST = []
    High_CDpwLIST = []
    Low_CDpwLIST = []
    sub_num = "003"
    
    with open (result_data_path + "003_pseudowordsDICT.json", "r", encoding = "utf-8") as jfile:
        pseudoDICT = json.load(jfile)
        pprint(pseudoDICT)
    
        #print(sub_num)
    
        targetPseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])
        High_CDpwLIST.extend(pseudoDICT["High_CD condition pseudowords_3"])
        Low_CDpwLIST.extend(pseudoDICT["Low_CD condition pseudowords_3"])
    
        print(sub_num, "Target pw : ", targetPseudoLIST)
        print(sub_num, "High-CD pw : ", High_CDpwLIST)
        print(sub_num, "Low-CD pw : ", Low_CDpwLIST) # output: 003 Low-CD pw :  ['vaesow', 'payliy', 'paenliy']
        """
    
    
        # Self_rating section
        readingLIST = []
        ratingDICT = {}
        count = 0
        cleaned_LIST = []
        textLIST = []
    
        # Load in the self-rating score
        with open (result_data_path + "{}_Reading_task.csv".format(sub_num), "r", encoding= 'unicode_escape') as csvfile_reading:  #, "r", encoding = "utf-8")
            readingLIST = csvfile_reading.read().split("\n")
            #pprint(readingLIST)
            #print(type(readingLIST))
            #print(len(readingLIST))
            readingLIST.pop(0)    # exclude the headers
            #print(len(readingLIST))
        
            # exclude the blank row
            readingLIST = LISTblankEraser(readingLIST)
            #print(len(readingLIST))
        
            # Divided the item in str type into 2 part for finding out the text
            for row in readingLIST:
                # Check the puntuation to split the text
                if ',"[""' in row:
                    rawLIST = row.split(',"[""')
                elif ',"[\'' in row:
                    rawLIST = row.split(',"[\'')
                    # if there's new type of punctuation, the script would let you know the str item hasn't been split
                else:
                    print("Wrong!!!!!!!!!!!!!!!!!! >>>>>",rawLIST)
                    print("Wrong_count >>>>>", len(rawLIST))
            
                # Check if the rawLIST been properly divided
                if len(rawLIST) ==2:
                    count +=1
                else:
                    print("Wrong!!!!!!!!!!!!!!!!!! >>>>>",rawLIST)
                    print("Wrong_count >>>>>", len(rawLIST))
                cleaned_LIST.append(rawLIST)
            
            print(count)
            #pprint(cleaned_LIST)
            print(len(cleaned_LIST))
        
            # to check the PWs that are in each text
            for row in cleaned_LIST:
                # lowercase all the words, split them into each word per unit
                textLIST = row[1].lower().split(" ")
                #print(textLIST)
                #print(len(textLIST))
            
                # print out the PWs according to the squence of the text and their CD condition
                for word in textLIST:
                    #print(word)
                    if word in High_CDpwLIST:
                        print(cleaned_LIST.index(row), "High-CD", word)
                    if word in Low_CDpwLIST:
                        print(cleaned_LIST.index(row), "Low-CD", word)
                    else:
                        pass
                
            # set out the count and blank LIST for further use
            count_H = 0
            count_L = 0
            H_textLIST = []
            L_textLIST = []
            new_H_textLIST = []
            new_L_textLIST = []
            H_ratingDICT = {}
            L_ratingDICT = {}
        
            # collect the H & L CD text based on the set PWs
            for row in cleaned_LIST:
                textLIST = row[1].lower().split(" ")
            
                # to go through each word inside each text for finding whether the pw is in the H- or L-CD_pwLIST, and then put those info into LIST by their CD types
                for word in textLIST:
                    # if the pw is one of the H-CD pw, then we would put this trial as the H_textLIST, also ignor other words that inside the same text
                    for H_pw in High_CDpwLIST:
                        if H_pw in word:
                            #print("High-CD", word)
                            count_H += 1
                            H_textLIST.append(row)
                        else:
                            pass
                
                    # if the pw is one of the H-CD pw, then we would put this trial as the H_textLIST, also ignor other words that inside the same text
                    for L_pw in Low_CDpwLIST:
                        if L_pw in word:
                            #print("Low-CD", word)
                            count_L += 1
                            L_textLIST.append(row)
                        else:
                            pass
                
            #print("count_H", count_H)
            #print("count_L", count_L)
            #print("Text_Hs", H_textLIST)
            #print(len(H_textLIST))
            #print("Text_Ls", L_textLIST)
            #print(len(L_textLIST))
            ##print(len(readingLIST[0]))
        
            # to accumulate the rating score according to the CD types
            for row in H_textLIST:
                rawLIST = row[0].split(",")
                rawLIST.append(row[1])
                new_H_textLIST.append(rawLIST)
                #print(new_H_textLIST)
                #print(len(new_H_textLIST))
        
            for row in L_textLIST:
                rawLIST = row[0].split(",")
                rawLIST.append(row[1])
                new_L_textLIST.append(rawLIST)
            #print(new_L_textLIST)
            #print(len(new_L_textLIST))
        
            # calculate the self-rating mean of H & L CD texts
            H_ratingDICT = Mean(new_H_textLIST, 4, "H-CD self-rating")
            L_ratingDICT = Mean(new_L_textLIST, 4, "L-CD self-rating")
        
            print(H_ratingDICT)
            print(L_ratingDICT)