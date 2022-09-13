#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# The normal packages for nlp
from pprint import pprint
import csv
import json
import random
from random import sample
from datetime import datetime,date
import pandas as pd
from collections import Counter

# TRF required packages
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import scipy.io as sio
from scipy import stats
import numpy as np
import mne
import eelbrain
from itertools import islice

"""
# Things that need to be prepared to do TRF
1. wordVec: the list of the content word in the text.
2. onset time of the word
3. offset time of the word
4. Sentence boundaries >> this one need to be calculate by myself >> the info is in the csv file.
CPS (closure positive shift), happened when the boundary started. 

the parameters of the envolope of the audio files need to be collect, then to downsample to 128 Hz.
** Alice's audio need to be downsample and calculate the envelope

mastoid channels >> use the soft bone behind both ears as the references (M1 / M2)

DC mode> without high pass filter >> add it on in the later analysis

EEG needs to match with the envelope data
"""



# Self-defined function by Kevin Hsu
def get_raw_EEG(Sid, runid):
    '''
    Get the raw data from the .mat file form, and do a several preprocessing steps
    '''
    audio = sio.loadmat("data/Stimuli/Envelopes/audio%d_128Hz.mat"%runid)
    text = sio.loadmat("data/Stimuli/Text/Run%d.mat"%runid)
    EEG = sio.loadmat("data/EEG/Subject%d/Subject%d_Run%d.mat"%(Sid,Sid,runid))
    eeg_scalp = EEG["eegData"] # time by channels
    eeg_mas = EEG["mastoids"]

    # time by channels >> channels by times
    eeg_scalp = np.transpose( eeg_scalp, (1, 0)) 
    eeg_mas = np.transpose( eeg_mas, (1, 0)) 

    eeg_ = np.concatenate((eeg_scalp, eeg_mas), axis = 0)
    audio = audio["env"]
    if eeg_.shape[1] > audio.shape[0]:
        eeg_ = eeg_[:, :audio.shape[0]]

    if eeg_.shape[1] < audio.shape[0]:
        audio = audio[:eeg_.shape[1]]

    tstep = 1. / 128
    n_times = audio.shape[0]
    time = eelbrain.UTS(0, tstep, n_times)
    envelope = eelbrain.NDVar(audio.ravel(), (time,), name='envelope')

    temp = mne.channels.make_standard_montage("biosemi128")
    ch_names = temp.ch_names
    ch_names.append("M1")
    ch_names.append("M2")
    ch_types = ['eeg'] * 130
    info = mne.create_info(ch_names, ch_types=ch_types, sfreq=128)

    raw = mne.io.RawArray(eeg_ * 1e-6, info)
    raw.set_eeg_reference(["M1", "M2"]).pick('all', exclude=["M1", "M2"]).set_montage('biosemi128')
    print(raw)

    return raw, envelope, time

def raw2NDvar(raw, time):
    '''
    Turn the raw data in NDVar form so that the 
    '''
    montage_x = eelbrain.load.fiff.sensor_dim(raw.info)
    temp_data = raw.get_data().T *1e+6
    eegNDVar = eelbrain.NDVar(temp_data, (time, montage_x), name='EEG', info={'unit': 'µV'})
    return eegNDVar

def word_onsets_NDVar(runid, time):
    text = sio.loadmat("data/Stimuli/Text/Run%d.mat"%runid)
    words = [x[0][0] for x in text["wordVec"]]
    onsets = [x[0] for x in text["onset_time"]]

    onset_word = eelbrain.NDVar(np.zeros(len(time)), time, name='Word_on')
    for x in onsets:
        onset_word[x] = 1
        pass
    return onset_word


if __name__ == "__main__":
    
    # After the neural data has been preprocessed(ICA)
    '''
    ICA(derivatives_in open data):
    1. remove the noise
    2. remove the motion artifacts
    '''
