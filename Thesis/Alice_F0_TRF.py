#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pathlib import Path
import re
import csv
import json
import pandas as pd
import time
from pprint import pprint
import numpy as np

import eelbrain
import mne
#import trftools


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

"""
def str2float(rawLIST):
    '''
    Turn the float(in str type) into actual float and save it into a LIST
    '''
    n_LIST = []
    for row in rawLIST:
        if float(row) ==True:
            n_float = float(row)
            n_LIST.append(n_float)
        else:
            print("This is not a float")
    n_LIST = rawLIST
    return n_LIST
"""

if __name__ == "__main__":
    
    STIMULI = [str(i) for i in range(1, 13)]
    #DATA_ROOT = Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")  #Path("~").expanduser() / 'Data' / 'Alice'
    DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")
    PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors'
    PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    EEG_DIR = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESL_ICAed_fif'
    F0_DIR = DATA_ROOT/ "TRFs_pridictors/IF_predictors"
    F0_DIR = DATA_ROOT/ "TRFs_pridictors/F0_predictors"
    IMFsLIST = [path.name for path in F0_DIR.iterdir() if re.match(r'Alice_IF_F0_*', path.name)]    
    SUBJECTS = [path.name for path in EEG_DIR.iterdir() if re.match(r'n_2_S\d', path.name)]  #S01_alice-raw.fif
    # Define a target directory for TRF estimates and make sure the directory is created
    TRF_DIR = DATA_ROOT / 'TRFs_ESLs'
    TRF_DIR.mkdir(exist_ok=True)
    #print(SUBJECTS)
    
    
    #[<NDVar 'envelope': 5863 time>, <NDVar 'envelope': 6194 time>, <NDVar 'envelope': 6435 time>, <NDVar 'envelope': 7108 time>, 
    # <NDVar 'envelope': 6737 time>, <NDVar 'envelope': 6487 time>, <NDVar 'envelope': 6399 time>, <NDVar 'envelope': 5840 time>, 
    # <NDVar 'envelope': 5832 time>, <NDVar 'envelope': 6236 time>, <NDVar 'envelope': 5726 time>, <NDVar 'envelope': 4808 time>]
    #[<NDVar 'envelope': 73665 time>]
    
    
    F0_lengthLIST = [5863, 6194, 6435, 7108, 6737, 6487, 6399, 5840, 5832, 6236, 5726, 4808]
    F0_NDVar = []
    for seqINT in range(1, 13):
        F0_seqINT = seqINT
        
        #F0_array = np.array()
        n_F0_fileLIST = []
        n_F0_LIST = []
        with open (F0_DIR / Path("Alice_%s_F0.csv" %str(F0_seqINT)), "r", encoding = "utf-8") as F0_csvFile:
            F0_fileLIST = F0_csvFile.read().split("\n")
            F0_fileLIST = LISTblankEraser(F0_fileLIST)
            for F_zero_str in F0_fileLIST:
                F_zero_float = float(F_zero_str)
                n_F0_fileLIST.append(F_zero_float)
            #print(n_F0_fileLIST)
            #print(type(n_F0_fileLIST[3]))
            F0_fileLIST = n_F0_fileLIST
            print(F0_fileLIST)
            print(type(F0_fileLIST[3]))
        
        pre_stimLIST = [0]*10  # = -0.100 ms 's timpoints
        
        # Add zero on the biginning of F0
        n_F0_LIST.extend(pre_stimLIST)
        #print("1", n_F0_LIST)
        #print(len(n_F0_LIST))
        
        # Add the F0 after the 10 zeros
        n_F0_LIST.extend(F0_fileLIST)
        #print("2", n_F0_LIST)
        
        # Add almost 1 s of timepoints after the F0
        F0_lengthINT = F0_lengthLIST[seqINT-1]
        #print(F0_lengthINT)
        if len(n_F0_LIST) < F0_lengthINT:
            left_F0_points = F0_lengthINT - len(n_F0_LIST)
            #print(left_F0_points)
            post_stimLIST = [0]*left_F0_points  # = + 1 s 's timpoints
            n_F0_LIST.extend(post_stimLIST)
            #print("3", len(n_F0_LIST))
        else:
            pass

        # Create the F0 TRF
        # Turn the list into array so that the following TRF would contain num instead of str
        n_F0_array = np.array(n_F0_LIST) # turn the str list into array
        pprint(n_F0_array)
        print(len(n_F0_array))
        #print(len(n_F0_LIST))
        #print(n_F0_LIST[seqINT-1])
        
        #for i in range(12):
        tstep = 1/100  # sampling rate's 倒數
        n_times = len(n_F0_array)  #original: len(n_F0_LIST)
        time = eelbrain.UTS(0, tstep=tstep, nsamples=n_times) # UTS(-0.1, tstep=tstep, nsamples=n_times+100)
        print(time)
        print(type(time))
        tmpF0_ = eelbrain.NDVar(n_F0_array, (time,), name='Fzero') #Original: eelbrain.NDVar(n_F0_LIST, (time,), name='Fzero')
        #F0_ = eelbrain.pad(tmpF0_, tstart=-0.100, tstop=tmpF0_.time.tstop + 1, name='F0_1')
        F0_NDVar.append(tmpF0_)
        print(type(tmpF0_))
        print(np.shape(tmpF0_))
    print(F0_NDVar)
    print(type(F0_NDVar))
    
    # save the F0 into pickle files
    F0_save_path = DATA_ROOT/ "TRFs_pridictors/F0_predictors" / Path("n_Alice_F0_all.pickle")
    eelbrain.save.pickle(F0_NDVar, F0_save_path)
    #"""
    """
    ## Check the saved csv
    #with open (F0_DIR / f'Alice_1_F0.csv') as F_zero_csv:
        #tmpF0_LIST = F_zero_csv.read().split("\n")
        #for F_zero_num in tmpF0_LIST[:20]:
            #print(F_zero_num)
            #print(type(F_zero_num))
        #pprint(tmpF0_LIST)
        
    """
    """
    # Check the datatype of the F0 saved in the pickle file
    F_zero_pickle = eelbrain.load.unpickle(F0_DIR / f'n_Alice_F0_all.pickle')
    for tmp in F_zero_pickle:
        ##n_tmp = np.array(tmp)
        n_tmp = eelbrain.NDVar(tmp, time, name='Fzero')
        pprint(n_tmp)
        print(type(n_tmp))
    pprint(F_zero_pickle)
    pprint(type(F_zero_pickle)) # str672 >> where went wrong?
    #"""
