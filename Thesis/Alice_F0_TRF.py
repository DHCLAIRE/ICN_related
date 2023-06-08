#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""This script estimates TRFs for several models and saves them"""
from pathlib import Path
import re

import eelbrain
import mne
import trftools

import numpy as np

if __name__ == "__main__":
    
    STIMULI = [str(i) for i in range(1, 13)]
    #DATA_ROOT = Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")  #Path("~").expanduser() / 'Data' / 'Alice'
    DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")
    PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors'
    PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    EEG_DIR = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESL_ICAed_fif'
    IMF_DIR = DATA_ROOT/ "TRFs_pridictors/IF_predictors"
    F0_DIR = DATA_ROOT/ "TRFs_pridictors/F0_predictors"
    IMFsLIST = [path.name for path in IMF_DIR.iterdir() if re.match(r'Alice_IF_IMF_*', path.name)]    
    SUBJECTS = [path.name for path in EEG_DIR.iterdir() if re.match(r'n_2_S\d', path.name)]  #S01_alice-raw.fif
    # Define a target directory for TRF estimates and make sure the directory is created
    TRF_DIR = DATA_ROOT / 'TRFs_ESLs'
    TRF_DIR.mkdir(exist_ok=True)
    print(SUBJECTS)
    
    F0_seqINT = 1
    
    with open (F0_DIR / Path("Alice_%s_F0.csv" %))