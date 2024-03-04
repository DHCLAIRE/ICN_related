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
        print(pic_pathSTR)
        # To change the backward slash('\\') into forward slash('/'), so that the Path(datapath) may be easily found in both Windows & Mac system
        pic_pathSTR = pic_pathSTR.replace('\\', "/", 30)
        #pic_typeSTR = pic_infoLIST[1]
        
        
        # Rename the file
        # src: The source file path (the existing file to be renamed).
        # dst: The destination file path (the new filename for the file).
        """
        pic_infoLIST[4] = gender   e.g. female & male               (F/M)
        pic_infoLIST[5] = race     e.g. black & caucasion & asian   (B/C/A)
        pic_infoLIST[6] = emotion  e.g. angry & fearful & neutral   (A/F/M)
        """
        
        ## Regroup the pics based on the emotions
        # Determine the emotion category
        if pic_infoLIST[6] == "angry":
            sub_emoSTR = "A"
        if pic_infoLIST[6] == "fearful":
            sub_emoSTR = "F"
        if pic_infoLIST[6] == "neutral":
            sub_emoSTR = "N"
        else:
            pass
        
        # Determine the gender category
        if pic_infoLIST[4] == "female":
            sub_genderSTR = "F"
        if pic_infoLIST[4] == "male":
            sub_genderSTR = "M"
        else:
            pass
        
        # Determine the race category
        if pic_infoLIST[5] == "black":
            sub_raceSTR = "B"
        if pic_infoLIST[5] == "caucasion":
            sub_raceSTR = "C"
        if pic_infoLIST[5] == "asion":
            sub_raceSTR = "A"
        else:
            pass
            
            
        new_picnameSTR = "%s_%s%s_%d" %(sub_emoSTR, sub_genderSTR, sub_raceSTR, "loop_num") # put in the real loop_num first
        
        # Put the pics into different folder based on emotion types
        if sub_emoSTR == "A":
            n_picFolder_path = root_data_path / "faces" / Path("Angry_emotion" %(sub_id, sub_cond))
            n_picFolder_path.mkdir(exist_ok=True)
            src = face_data_path  # old file name
            dst = n_picFolder_path # new file name
            os.rename(src, dst, src_dir_fd=None, dst_dir_fd=None)