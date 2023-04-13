#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
import csv
import json
import random
from random import sample
import os
from gtts import gTTS
import pandas as pd
import time
from pathlib import Path

"""
# for audio file alternation
from scipy.io import wavfile
import scipy.signal
from pydub import AudioSegment
"""

def LISTblankEraser(rawLIST):
    '''
    Remove the blank that inside the list
    '''
    newrawLIST = []
    for row in rawLIST:
        if len(row) == 0:
            rawLIST.pop(rawLIST.index(row))
        else:
            pass
    newrawLIST = rawLIST
    #print(len(newrawLIST))
    return newrawLIST

if __name__ == "__main__":
    LTTCroot_data_path = Path("/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG")
    Thesisroot_data_path = Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")
    
    word_LIST = []
    
    for sub_id in range(1):
        sub_idINT = sub_id+1
        text_data_path = LTTCroot_data_path / ("LTTC_MEG_S%.3d" %sub_idINT)
        
        # Open the csv fule
        with open (text_data_path / Path("S%.3d_Reading_task.csv" %sub_idINT), "r", encoding = "utf-8") as csvfile:
            fileLIST = csvfile.read().split("\n")
            fileLIST = LISTblankEraser(fileLIST)
            print(len(fileLIST))
            print(fileLIST)
            
            # Call out every text per subject
            for row in fileLIST:
                print(row)
                per_textLIST = row.split(',"[')
                print(per_textLIST)
            

                """
                # making the wanted info into the List form for future use
                sub_idLIST.append(sub_id)
                dateLIST.append(day)
                sub_condLIST.append(sub_cond)
                roundLIST.append(round_)
                stimLIST.append(stim_wordSTR)
                CD_condLIST.append(cdSTR)
                resultKeyLIST.append(keys)
                responseLIST.append(conditionLIST)
                LDT_rtLIST.append(time_duration)
                correctnessLIST.append(correctLIST)
            
        #Display the instruction of the break in between Round 1 & Round 2
        print("Round", round_, "is over.")
        if round_ == 1:
            display_ins(instructions_3, keypressLIST_space)
        else:
            display_ins(instructions_4, keypressLIST_space)

            # close the window  at the end of the experiment
    win.close()


    # Saving the self_paced_rt result into csv file
    dataDICT = pd.DataFrame({'Sub_id':sub_idLIST,
                           'Date':dateLIST,
                           'Sets':sub_condLIST,
                           'Round':roundLIST,
                           'Stimuli':stimLIST,
                           'CD_condition':CD_condLIST,
                           'Keypress':resultKeyLIST,
                           'Response':responseLIST,
                           'LDT_RT':LDT_rtLIST,
                           'Correctness':correctnessLIST
                           })

    #data_path = "/Users/ting-hsin/Docs/Github/ICN_related/"
    file_name = 'S%s_LDT_preschool_testing_results.csv' %sub_id
    save_path = result_data_path / Path(file_name)
    dataDICT.to_csv(save_path, sep = "," ,index = False , header = True, encoding = "UTF-8")

"""