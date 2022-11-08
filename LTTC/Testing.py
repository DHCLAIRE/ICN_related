#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import csv
from pprint import pprint

#from psychopy import prefs
#prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

#import psychtoolbox as ptb
#from psychopy import sound, core, visual, event, gui, monitors, clock, parallel  #, parallel   # if you change the setting, this command must be put after the prefs's command
##import json
#print(sound.Sound)


import scipy
from scipy.io import wavfile
import numpy as np
from datetime import datetime,date
import json
import numpy as np
import pandas as pd
from pprint import pprint



if __name__ == "__main__":
    """
    sub_id = str(input("Subject: "))
    
    result_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S%s/" %sub_id # Testing
    
    with open(result_data_path + "S%s_Reading_task.csv" %sub_id, "r", encoding="UTF-8") as csvfile:  #, newline=''
        result_csvLIST = csvfile.read().split("\n")
        pprint(result_csvLIST)
    """
    """
    # Inspecting the dtype of the wav file
    data_path = "/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Alice(EEG dataset_mat_and stimuli)/audio/"
    data_path_1 = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG/LTTC_MEG_S001/S001_audios/"
    
    LTTC_stm_old = data_path_1 + "S001_textaudio_modified_1.wav"
    LTTC_stm_new = data_path_1 + "S001_modified_1.wav"
    Alice_stm = data_path + "DownTheRabbitHoleFinal_SoundFile1.wav"
    
    sample_rate, data = wavfile.read(Alice_stm)
    sample_rate_1, data_1 = wavfile.read(LTTC_stm_old)
    sample_rate_2, data_2 = wavfile.read(LTTC_stm_new)
    print("Alice sampling_R=",sample_rate)
    print("LTTC old sampling_R=",sample_rate_1)
    print("LTTC new sampling_R=",sample_rate_2)
    #print(data)
    print(type(data))
    print(type(data_1))
    print(type(data_2))
    x = data.dtype
    y = data_1.dtype
    z = data_2.dtype
    print(x)
    print(y)
    print(z)
    """
    #"""
    numLIST = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16 ,17 ,18 ,19 ,20], [21, 22, 23, 24, 25], [26, 27, 28, 29, 30]]
    # How to create a string in a 2 layers loop
    for i in range(6):
        for k in range(5):
            numSTR = str(numLIST[i][k])  # new version (5 tapes per unit)
            #numSTR = str(int("%d%d" %(i, k))+1) # old version (10 tapes per unit)
            #numSTR = "%02d" %(i)  # automatically fill the zero on the left side of the number if the number didn't meer 2 digits
            print(numSTR)
            #"""