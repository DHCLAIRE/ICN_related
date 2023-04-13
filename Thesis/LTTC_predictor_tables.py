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

if __name__ == "__main__":
    LTTCroot_datapath = Path("/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_MEG")
    Thesisroot_datapath = Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")
    for sub_id in range(1):
        sub_idINT = sub_id+1
        text_data_path = LTTCroot_datapath / Path("LTTC_MEG_S%.3d" %sub_idINT)
        
        textCSV = text_data_path / Path("S%.sd_Reading_task.csv" %sub_idINT)
        print(sub_idINT)
        print(text_data_path)
        #result_data_path = root_data_path / 

