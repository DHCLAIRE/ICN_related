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
import statistics

def LISTblankEraser(rawLIST):
    '''
    Remove the blank item inside the list
    '''
    newrawLIST = []
    for row in rawLIST:
        if len(row) == 0:
            rawLIST.pop(rawLIST.index(row))
        else:
            pass
    newrawLIST = rawLIST
    return newrawLIST

def get_List(resultLIST, i):
    '''
    Extract the wanted data from the raw data LIST
    '''
    contentLIST = []
    for row in resultLIST:
        if type(row) == list:
            rawLIST = row
            contentLIST.append(float(rawLIST[i]))
        else:
            rawLIST = row.split(",")
            contentLIST.append(float(rawLIST[i]))
    return contentLIST

def remove_value(contentLIST, value):
    '''
    Exclude the missing_value
    '''
    for k in contentLIST:
        if float(value) in contentLIST:
            contentLIST.remove(float(value))
        else:
            pass
    return contentLIST

def get_NA_count(A_LIST, countINT):
    '''
    Get the excluded N/A count
    '''
    raw_count = len(A_LIST)
    if raw_count != countINT:
        exclude_countINT = countINT - raw_count
    else:
        exclude_countINT = 0
        
    return exclude_countINT

def Mean(resultLIST):
    meanFLOAT = round(np.mean(np.array(resultLIST)), 3)
    return meanFLOAT

def STD(resultLIST, df):
    stdFLOAT = round(np.std(np.array(resultLIST), ddof = df),3)
    return stdFLOAT

"""
def Mean(resultLIST, item_index, missing_value, total_count, typeSTR = None):
    '''
    Get the mean of the cleaned data list
    '''
    contentLIST = get_List(resultLIST, item_index)
    contentLIST = remove_value(contentLIST, missing_value)
    NA_count = get_NA_count(contentLIST, total_count)
    meanFLOAT = round(np.mean(np.array(contentLIST)), 3) #ouput: H pwRT Mean : 783.167
    MeanDICT = {"{} count".format(typeSTR):len(contentLIST),"{} Mean".format(typeSTR):meanFLOAT , "Exclude 0.0 count": NA_count}
    
    return MeanDICT

def STD(resultLIST, i, df, typeSTR = None):

    PLDTstd_subFLOAT = round(np.std(np.array(contentLIST), ddof = df),3) #ouput: H pwRT Mean : 783.167
    StdDICT = {"{} count".format(typeSTR):len(contentLIST),"{} STD".format(typeSTR):PLDTstd_subFLOAT, "Exclude 0.0 count": exclude_countINT}
    
    return StdDICT
"""

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
    
    sub_idLIST = []
    H_total_rawRT_LIST = []
    L_total_rawRT_LIST = []
    H_total_finalRT_LIST = []
    L_total_finalRT_LIST = []
    
    sub_AllrawCorrect_LIST = []
    H_total_rawCorrect_LIST = []
    L_total_rawCorrect_LIST = []
    H_total_finalCorrect_LIST = []
    L_total_finalCorrect_LIST = []    
    
    for z in range(3):
        # Setting up the data_path
        #result_data_path = "/Users/neuroling/Downloads/DINGHSIN_Results/2nd_Stim-results_selfPRT_PLDT/"
    
        resultLIST = []
        tmpLIST = []
    
        #剩把pseudoDICT的值叫出來
        pseudoLIST = []
        targetPseudoLIST = []
        High_CDpwLIST = []
        Low_CDpwLIST = []

        sub_num = "0{}".format(z+24)
        # Open the pseudowordDICT for the further indications
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
    
        '''
        ## WHOLE GROUP ##
        # Mean
        #H_PLDTmean_allLIST = []
        #L_PLDTmean_allLIST = []
        ## SD
        #H_PLDTsd_allLIST = []
        #L_PLDTsd_allLIST = []
    '''
    
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
        #print("H_CD_rawLIST", H_CD_rawLIST)  # [['022', '2022-05-14', 'aegliy', "['z']", "['seen']", '1982.0', "['True']"], ['022', '2022-05-14', 'vaesow', "['z']", "['seen']", '726.0', "['True']"],.....]]
        #print(len(H_CD_rawLIST))
        #print("L_CD_rawLIST", L_CD_rawLIST)  # same as "H_CD_rawLIST"
        #print(len(L_CD_rawLIST))
        
        
        # Calculate the RT Mean of the H & L PLDT
        
        # High CD condition
        H_RT_LIST = get_List(H_CD_rawLIST, 5)  #{'High-CD RT count': 30, 'High-CD RT Mean': 783.167, 'Exclude 0.0 count': 0}
        n_H_RT_LIST = H_RT_LIST.copy()
        n_H_RT_LIST = remove_value(n_H_RT_LIST, 0.0)
        H_RT_NA_count = get_NA_count(n_H_RT_LIST, len(H_CD_rawLIST))
        H_mean_subFLOAT = Mean(n_H_RT_LIST)   #round(np.mean(np.array(H_RT_LIST)), 3)
        H_std_subFLOAT = STD(n_H_RT_LIST, 1)  #round(np.std(np.array(H_RT_LIST), ddof = 1), 3)
        
        H_two_stdFLOAT = H_std_subFLOAT*2
        H_up_RT_range = H_mean_subFLOAT + H_two_stdFLOAT
        H_low_RT_range = H_mean_subFLOAT - H_two_stdFLOAT
        
        # remove values that outside 2 STD 
        for RT_FLOAT in n_H_RT_LIST:
            if RT_FLOAT > H_up_RT_range:
                n_H_RT_LIST = remove_value(n_H_RT_LIST, RT_FLOAT)
            if RT_FLOAT < H_low_RT_range:
                n_H_RT_LIST = remove_value(n_H_RT_LIST, RT_FLOAT)
            else:
                pass
        
        H_final_RT_NA_count = get_NA_count(n_H_RT_LIST, len(H_CD_rawLIST))
        H_final_mean_subFLOAT = Mean(n_H_RT_LIST)
        H_final_std_subFLOAT = STD(n_H_RT_LIST, 1)
        
        #print(len(H_RT_LIST))
        #print(len(n_H_RT_LIST))
        #print(H_RT_NA_count)
        #print(H_final_RT_NA_count)
        #print("{} H RT Mean:".format(sub_num), H_mean_subFLOAT)
        #print("{} H new RT Mean:".format(sub_num), H_final_mean_subFLOAT)
        #print("{} H RT SD:".format(sub_num), H_std_subFLOAT)
        #print("{} H new RT SD:".format(sub_num), H_final_std_subFLOAT)
        
        # Low CD condition
        L_RT_LIST = get_List(L_CD_rawLIST, 5)
        L_RT_LIST = remove_value(L_RT_LIST, 0.0)
        L_RT_NA_count = get_NA_count(L_RT_LIST, len(L_CD_rawLIST))
        L_mean_subFLOAT = Mean(L_RT_LIST)   #round(np.mean(np.array(H_RT_LIST)), 3)
        L_std_subFLOAT = STD(L_RT_LIST, 1)
        
        L_two_stdFLOAT = L_std_subFLOAT*2
        L_up_RT_range = L_mean_subFLOAT + L_two_stdFLOAT
        L_low_RT_range = L_mean_subFLOAT - L_two_stdFLOAT
        
        # remove values that outside 2 STD 
        for RT_FLOAT in L_RT_LIST:
            if RT_FLOAT > L_up_RT_range:
                L_RT_LIST = remove_value(L_RT_LIST, RT_FLOAT)
                #print("It's bigger!!!", RT_FLOAT)
            if RT_FLOAT < L_low_RT_range:
                L_RT_LIST = remove_value(L_RT_LIST, RT_FLOAT)
                #print("It's smaller!!!", RT_FLOAT)
            else:
                pass
            
        L_final_RT_NA_count = get_NA_count(L_RT_LIST, len(L_CD_rawLIST))
        L_final_mean_subFLOAT = Mean(L_RT_LIST)
        L_final_std_subFLOAT = STD(L_RT_LIST, 1)
        
        #print(L_RT_LIST)
        #print(L_RT_NA_count)
        #print(L_final_RT_NA_count)
        #print("{} L RT Mean:".format(sub_num), L_mean_subFLOAT)
        #print("{} L new RT Mean:".format(sub_num), L_final_mean_subFLOAT)
        #print("{} L RT SD:".format(sub_num), L_std_subFLOAT)
        #print("{} L new RT SD:".format(sub_num), L_final_std_subFLOAT)

        # Calculate the Correctness of all, and H & L PLDT, there's three in total 
        PLDT_correct_subDICT = correctness(resultLIST, "PLDT-total")
        H_PLDT_correct_subDICT = correctness(H_CD_rawLIST, "H-CD PLDT")
        L_PLDT_correct_subDICT = correctness(L_CD_rawLIST, "L-CD PLDT")
        
        
        print("{} PLDT H & Lcorrect:".format(sub_num), H_PLDT_correct_subDICT, ";", L_PLDT_correct_subDICT)
        n_H_CD_rawLIST = H_CD_rawLIST.copy()
        n_L_CD_rawLIST = L_CD_rawLIST.copy()
        
        # Excluding the 2STD in H condition
        for outsiderLIST in n_H_CD_rawLIST:
            if float(outsiderLIST[5]) > H_up_RT_range:
                print(n_H_CD_rawLIST.index(outsiderLIST))
                n_H_CD_rawLIST.pop(n_H_CD_rawLIST.index(outsiderLIST))
                
            if float(outsiderLIST[5]) < H_low_RT_range:
                print(n_H_CD_rawLIST.index(outsiderLIST))
                n_H_CD_rawLIST.pop(n_H_CD_rawLIST.index(outsiderLIST))
            else:
                pass
            
            
        # Excluding the 2STD in L condition
        for outsiderLIST in n_L_CD_rawLIST:
            if float(outsiderLIST[5]) > L_up_RT_range:
                print(n_L_CD_rawLIST.index(outsiderLIST))
                n_L_CD_rawLIST.pop(n_L_CD_rawLIST.index(outsiderLIST))
                
            if float(outsiderLIST[5]) < L_low_RT_range:
                print(n_L_CD_rawLIST.index(outsiderLIST))
                n_L_CD_rawLIST.pop(n_L_CD_rawLIST.index(outsiderLIST))
            else:
                pass
        
        n_H_PLDT_correct_subDICT = correctness(n_H_CD_rawLIST, "New H-CD PLDT")
        n_L_PLDT_correct_subDICT = correctness(n_L_CD_rawLIST, "New L-CD PLDT")
        
        #print("{} PLDT TOTAL_correct:".format(sub_num), PLDT_correct_subDICT)
        print("{} New PLDT H & Lcorrect:".format(sub_num), n_H_PLDT_correct_subDICT, ";", n_L_PLDT_correct_subDICT)
        
        # making the wanted info into the List form for future use
        sub_idLIST.append(sub_num)
        H_total_rawRT_LIST.append(H_mean_subFLOAT)
        L_total_rawRT_LIST.append(L_mean_subFLOAT)
        H_total_finalRT_LIST.append(H_final_mean_subFLOAT)
        L_total_finalRT_LIST.append(L_final_mean_subFLOAT)
        
        sub_AllrawCorrect_LIST.append(PLDT_correct_subDICT["PLDT-total Correctness"])
        H_total_rawCorrect_LIST.append(H_PLDT_correct_subDICT["H-CD PLDT Correctness"])
        L_total_rawCorrect_LIST.append(L_PLDT_correct_subDICT["L-CD PLDT Correctness"])
        H_total_finalCorrect_LIST.append(n_H_PLDT_correct_subDICT["New H-CD PLDT Correctness"])
        L_total_finalCorrect_LIST.append(n_L_PLDT_correct_subDICT["New L-CD PLDT Correctness"])
    
        # Saving the self_paced_rt result into csv file
        dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                                 'H_raw_RTMean':H_total_rawRT_LIST,
                                 'L_raw_RTMean':L_total_rawRT_LIST,
                                 'H_final_RTMean':H_total_finalRT_LIST,
                                 'L_final_RTMean':L_total_finalRT_LIST,
                                 'ALL_Correctness':sub_AllrawCorrect_LIST,
                                 'H_raw_Correctness':H_total_rawCorrect_LIST, 
                                 'L_raw_Correctness':L_total_rawCorrect_LIST, 
                                 'H_final_Correctness':H_total_finalCorrect_LIST, 
                                 'L_final_Correctness':L_total_finalCorrect_LIST
                                 })
    
    file_name = 'PLDT_analyzed_results.csv'
    save_path = result_data_path + file_name
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")
    
        #print("{} PLDT TOTAL_correct:".format(sub_num), PLDT_correct_subDICT)
        #print("{} PLDT H & Lcorrect:".format(sub_num), H_PLDT_correct_subDICT, ";", L_PLDT_correct_subDICT)
        
        #print("{} just PLDT figures:".format(sub_num), H_pwRT_DICT["High-CD RT Mean"], L_pwRT_DICT["Low-CD RT Mean"],PLDT_correct_subDICT["PLDT-total Correctness"],H_PLDT_correct_subDICT["H-CD PLDT Correctness"],L_PLDT_correct_subDICT["L-CD PLDT Correctness"])
        #print(H_pwRT_DICT["High-CD RT Mean"], L_pwRT_DICT["Low-CD RT Mean"],PLDT_correct_subDICT["PLDT-total Correctness"],H_PLDT_correct_subDICT["H-CD PLDT Correctness"],L_PLDT_correct_subDICT["L-CD PLDT Correctness"])
        
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
            
            #print(count)
            #pprint(cleaned_LIST)
            #print(len(cleaned_LIST))

            # set out the count and blank LIST for further use
            count_H = 0
            count_L = 0
            H_textLIST = []
            L_textLIST = []
            new_H_textLIST = []
            new_L_textLIST = []
            ALL_ratingDICT = {}
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
                            #print(cleaned_LIST.index(row), "High-CD", word)
                            count_H += 1
                            H_textLIST.append(row)
                        else:
                            pass
                
                    # if the pw is one of the H-CD pw, then we would put this trial as the H_textLIST, also ignor other words that inside the same text
                    for L_pw in Low_CDpwLIST:
                        if L_pw in word:
                            #print(cleaned_LIST.index(row), "Low-CD", word)
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
            ALL_ratingDICT = Mean(readingLIST, 4, "Total self-rating")
            H_ratingDICT = Mean(new_H_textLIST, 4, "H-CD self-rating")
            L_ratingDICT = Mean(new_L_textLIST, 4, "L-CD self-rating")
        
            print("{} self-rating :".format(sub_num), ALL_ratingDICT, ";",  H_ratingDICT, ";", L_ratingDICT)
            print("{} self-rating nums:".format(sub_num), ALL_ratingDICT["Total self-rating Mean"], H_ratingDICT["H-CD self-rating Mean"], L_ratingDICT["L-CD self-rating Mean"])

        with open (result_data_path + "{}_textsDICT.json".format(sub_num), "r", encoding = "utf-8") as jjfile:
            textsetsDICT = json.load(jjfile)
            print("{} H & L text set:".format(sub_num), textsetsDICT["The High-Low Set Group"])
            
            print('')
            """
        
        

    