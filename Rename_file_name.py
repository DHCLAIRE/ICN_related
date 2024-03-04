#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import os
import scipy
from scipy.io import wavfile
import numpy as np
from datetime import datetime,date
import json
import numpy as np
import pandas as pd
from pprint import pprint
import random
from random import sample
import re
from pathlib import Path
import serial


def gender(inputSTR):
    '''
    Determine the gender category
    '''
    sub_genderSTR = str()
    if inputSTR == "female":
        sub_genderSTR = "F"
    if inputSTR == "male":
        sub_genderSTR = "M"
    else:
        print("No gender")
    
    return sub_genderSTR

def race(inputSTR):
    '''
    Determine the race category
    '''
    sub_raceSTR = str()
    if inputSTR == "black":
        sub_raceSTR = "B"
    if inputSTR == "caucasian":
        sub_raceSTR = "W"
    if inputSTR == "asian":
        sub_raceSTR = "A"
    else:
        print("No race")
    
    return sub_raceSTR

def emotion(inputSTR):
    '''
    Determine the emotion category
    '''
    sub_emoSTR = str()
    if inputSTR == "angry":
        sub_emoSTR = "angry"
    if inputSTR == "fearful":
        sub_emoSTR = "fearful"
    if inputSTR == "neutral":
        sub_emoSTR = "neutral"
    else:
        print("No emotion")
    
    return sub_emoSTR




if __name__ == "__main__":
    # Set up the data path (For Mac)
    root_data_path = Path("/Users/ting-hsin/Downloads/MaterialsExp2")
    face_data_path = root_data_path / "faces"
    Bg_data_path = root_data_path / "Backgrounds"
    
    
    with open(root_data_path / 'n_material_files_faces_n_Bg.csv', 'r', encoding = "utf-8") as csvf:
        pic_fileLIST = csvf.read().split("\n")
        pprint(pic_fileLIST)
        pic_fileLIST.pop(0)
    
    pic_infoLIST = []
    for pic_info in pic_fileLIST: #[1:50]:
        pic_infoLIST = pic_info.split(",")
        print(pic_infoLIST, len(pic_infoLIST))
        
        # Extract the pic name out of the data path
        pic_pathSTR = pic_infoLIST[0]
        
        # To change the backward slash('\\') into forward slash('/'), so that the Path(datapath) may be easily found in both Windows & Mac system
        pic_pathSTR = pic_pathSTR.replace('\\', "/", 30)
        #pic_typeSTR = pic_infoLIST[1]
        print(pic_pathSTR)
        
        # Rename the file
        # src: The source file path (the existing file to be renamed).
        # dst: The destination file path (the new filename for the file).
        """
        pic_infoLIST[4] = gender   e.g. female & male               (F/M)
        pic_infoLIST[5] = race     e.g. black & caucasion & asian   (B/C/A)
        pic_infoLIST[6] = emotion  e.g. angry & fearful & neutral   (A/F/M)
        """
        
        #print(pic_infoLIST[4])
        #print(pic_infoLIST[5])
        #print(pic_infoLIST[6])
        
        count_FB_INT = 0
        count_FW_INT = 0
        count_FA_INT = 0
        count_MB_INT = 0
        count_MW_INT = 0
        count_MA_INT = 0
        genderSTR = gender(pic_infoLIST[4])
        raceSTR = race(pic_infoLIST[5])
        emotionSTR = emotion(pic_infoLIST[6])
        
        tmpSTR = raceSTR+genderSTR
        if tmpSTR == "FB":
            count_FB_INT=+1
        if tmpSTR == "FB":
            count_FB_INT=+1
        if tmpSTR == "FB":
                count_FB_INT=+1
        
        
        #tmp_picnameSTR = "%s_%s%s" %(emotionSTR, genderSTR, raceSTR) #, count_A_INT) # put in the real loop_num first
        #print(tmp_picnameSTR)

        
        #print(new_picnameSTR)
        
        """
        # Put the pics into different folder based on emotion types
        if sub_emoSTR == "A":
            n_picFolder_path = root_data_path / "faces" / Path("Angry_face" %(sub_id, sub_cond))
            n_picFolder_path.mkdir(exist_ok=True)
            src = face_data_path  # old file name
            dst = n_picFolder_path # new file name
            os.rename(src, dst, src_dir_fd=None, dst_dir_fd=None)
            
            """