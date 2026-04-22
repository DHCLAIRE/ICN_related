#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pathlib import Path
import re
import matplotlib.pyplot as plt
from matplotlib import pyplot
import eelbrain
import mne
#import trftools

from pprint import pprint
import numpy as np

if __name__ == "__main__":
    STIMULI = [str(i) for i in range(1, 13)]
    DATA_ROOT = Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")  #Path("~").expanduser() / 'Data' / 'Alice'
    PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors'
    PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    EEG_DIR = DATA_ROOT / 'EEG_Natives' / 'Alice_natives_ICAed_fif'
    Native_SUBJECTS = [path.name for path in EEG_DIR.iterdir() if re.match(r'S\d*', path.name)]
    # Define a target directory for TRF estimates and make sure the directory is created
    TRF_DIR = DATA_ROOT / 'TRFs_Natives'
    TRF_DIR.mkdir(exist_ok=True)
    print(Native_SUBJECTS)
    print(len(Native_SUBJECTS))
    
    n_rowsLIST = []
        
    for subj in Native_SUBJECTS:
        n_subj = int(subj[1:3])
        trf = eelbrain.load.unpickle(TRF_DIR / Path('S%.2d/S%.2d envelope.pickle'%(int(subj[1:3]), int(subj[1:3]))))
        #print(trf.h[0])
        #print(trf.h_scaled)
        print(trf.x_mean)
        n_rowsLIST.append([n_subj, trf.proportion_explained, trf.h[0]])#.abs()])